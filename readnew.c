#include <string.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <pcap.h>

#define BUFF_LEN 1024
struct node
{
	char src[40];
	char dst[40];
	int total;
	struct node *next;
};

struct node* headNode;

void print_statics(struct node * head)
{
	FILE *fp;
	fp=fopen("plotlog.txt","w");
	while(head->next!=NULL){
		fprintf(fp,"%s %s %d\n", head->src,head->dst,head->total);
		head=head->next;
	}
	fclose(fp);
}

void httppcap_http_process(uint32_t clientip, uint32_t serverip, uint16_t clientport, uint16_t serverport, const unsigned char *data) {
	//Record headNode
	printf("Waring:mining packets detected:\n");
    printf("From: %s:%u\t", inet_ntoa(*(struct in_addr *)&clientip), clientport);
    printf("To: %s:%u\n", inet_ntoa(*(struct in_addr *)&serverip), serverport);
    printf("Payload: %s\n", data);  
	struct node *currentNode=headNode;
	int creat=1;
	//Initialize headnode
	if(headNode->next==NULL)
	{
		strcpy(headNode->src,inet_ntoa(*(struct in_addr *)&clientip));
		strcpy(headNode->dst,inet_ntoa(*(struct in_addr *)&serverip));
		headNode->total=1;
		headNode->next=(struct node *)malloc(sizeof(struct node));
		headNode->next->next=NULL;
	}
	else{
		while(currentNode->next!=NULL){
			if(((strcmp(currentNode->src,inet_ntoa(*(struct in_addr *)&clientip)))==0)&((strcmp(currentNode->dst,inet_ntoa(*(struct in_addr *)&serverip)))==0))
			{
				currentNode->total+=1;
				creat=0;
				break;
			}
			else
				currentNode=currentNode->next;
		}
		if(creat)
		{
			strcpy(currentNode->src,inet_ntoa(*(struct in_addr *)&clientip));
			strcpy(currentNode->dst,inet_ntoa(*(struct in_addr *)&serverip));
			currentNode->total=1;
			currentNode->next=(struct node *)malloc(sizeof(struct node));
			currentNode->next->next=NULL;			
		}
	}      
}

void dispatcher_handler(u_char *,const struct pcap_pkthdr *, const u_char *);

int main(int argc, char *argv[])
{
	headNode=(struct node *)malloc(sizeof(struct node));
	pcap_t *source_pcap_t=NULL;
	//打开要处理pcap文件
	char errbuf[PCAP_ERRBUF_SIZE]={0};
	if( (source_pcap_t=pcap_open_offline(argv[1], errbuf))==NULL )
	{
		printf("pcap_open_offline() return NULL.\nerrbuf:%s\n", errbuf);
		return;
	}
	pcap_loop(source_pcap_t,0,dispatcher_handler,NULL);
	pcap_close(source_pcap_t);
	print_statics(headNode);
	return 0;
}

void dispatcher_handler(unsigned char *arg,const struct pcap_pkthdr *pkthdr, const unsigned char *bytes)
{
	uint32_t srcip, dstip;
	uint16_t srcport, dstport;	
    // Check minimum packet size
    // 14 (Ethernet) + 20 (IPv4) + 20 (TCP) = 54
    if (pkthdr->len < 54)
       	return;
    	
    // Determine ethernet header length
    unsigned short ethhdrlen = 14;
    unsigned short ethertype = 0;
   	if (bytes[12] == 0x81 && bytes[13] == 0x00)
	{
		// VLAN tag
		ethhdrlen = 18;
		ethertype = (bytes[16] << 8) | bytes[17];
	/* TODO: Support for double tagging, etc. */
	} 
	else
		ethertype = (bytes[12] << 8) | bytes[13];
	// IP and TCP header processing
	uint8_t iphdrlen, tcphdrlen;
	
	switch (ethertype)
	{
		case 0x0800:
		    // IPv4
		    iphdrlen = (bytes[ethhdrlen] & 0x0F) << 2;
		    if (iphdrlen < 20)
				return;
		    // Require: TCP	    
		    if (bytes[ethhdrlen + 9] != 6)
		    	return;
			srcip = *(uint32_t*)& bytes[ethhdrlen + 12];
			dstip = *(uint32_t*)& bytes[ethhdrlen + 16];
		    // TCP
		    // PSH
			if (!(bytes[ethhdrlen + iphdrlen + 13] & 0x08))
				return;
			tcphdrlen = (bytes[ethhdrlen + iphdrlen + 12] & 0xF0) >> 2;
			srcport = ntohs(*(uint16_t*)& bytes[ethhdrlen + iphdrlen]);
			dstport = ntohs(*(uint16_t*)& bytes[ethhdrlen + iphdrlen + 2]);
		    break;
		default:
	    	return;
	}
	const unsigned char * payload = bytes + ethhdrlen + iphdrlen + tcphdrlen;
	if (payload[0] == '\0')
        return;
	int flag = 0;
        if (strstr(payload, "blob"))
       	    flag = 1;
	else if (strstr(payload, "nonce"))
		flag = 1;
        else if (strstr(payload, "mining"))
                flag = 1;
	if (!flag)
		return;
	httppcap_http_process(srcip, dstip, srcport, dstport, payload);
} 
