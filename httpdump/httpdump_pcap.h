#ifndef _HTTPPCAP_PCAP_
#define _HTTPPCAP_PCAP_

#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <pcap.h>
#include <arpa/inet.h>

void httppcap_http_process(uint32_t clientip, uint32_t serverip, uint16_t clientport, uint16_t serverport, const unsigned char* data)
{
	printf("Waring:mining packet detected:\n");
	printf("From: %s:%u\t", inet_ntoa(*(struct in_addr*) & clientip), clientport);
	printf("To: %s:%u\n", inet_ntoa(*(struct in_addr*) & serverip), serverport);
	printf("Payload: %s\n", data);
}

/*
 * Packet handler
 */
void PacketArrival (unsigned char *arg, const struct pcap_pkthdr *pkthdr, const unsigned char *bytes) {
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

/*
 * Pcap Initialization
 */
void httppcap_pcap_start (char *dev) {

    char errbuf[PCAP_ERRBUF_SIZE];
    
    if (dev == NULL) {
        // Use default device
        dev = pcap_lookupdev(errbuf);
        if (dev == NULL) {
            fprintf(stderr, "Error: cannot get default device: %s\n", errbuf);
            exit(1);
        }
    }
    
    printf("Opening device %s...\n", dev);
    
    pcap_t *handle;
    handle = pcap_open_live(dev, 65535, 1, 1000, errbuf);
    
    if (handle == NULL) {
        // Unable to open a live capturing device
        // Try offline device
        handle = pcap_open_offline(dev, errbuf);
        if (handle == NULL) {
            fprintf(stderr, "Error: cannot open device %s: %s\n", dev, errbuf);
            exit(1);
        }
        struct bpf_program fp;
        char filter_exp[] = "tcp";
                if (pcap_compile(handle, &fp, filter_exp, 0, 0) == -1) {
                        fprintf(stderr, "Error: cannot parse filter %s: %s\n", filter_exp, pcap_geterr(handle));
                        exit(1);
                }
                if (pcap_setfilter(handle, &fp) == -1) {
                        fprintf(stderr, "Error: cannot install filter %s: %s\n", filter_exp, pcap_geterr(handle));
                        exit(1);
                }
    } else {
    	struct bpf_program fp;
    	char filter_exp[] = "tcp";
		if (pcap_compile(handle, &fp, filter_exp, 0, 0) == -1) {
			fprintf(stderr, "Error: cannot parse filter %s: %s\n", filter_exp, pcap_geterr(handle));
			exit(1);
		}
		if (pcap_setfilter(handle, &fp) == -1) {
			fprintf(stderr, "Error: cannot install filter %s: %s\n", filter_exp, pcap_geterr(handle));
			exit(1);
		}
    }
    
    // Loop and call PacketArrival() for received packets
    pcap_loop(handle, -1, PacketArrival, NULL);
    
}

#endif //_HTTPPCAP_PCAP_

