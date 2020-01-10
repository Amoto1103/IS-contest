#include <stdlib.h>
#include <stdio.h>
#include <getopt.h>
#include "httpdump_pcap.h"

/*
 * Displays help message
 */
void usage () {
    printf("Usage: httpdump [-i <interface>]\n");
}

/*
 * Main
 */
int main (int argc, char *argv[]) {
    
    char *interface = NULL;
        
    int c;
    while ((c = getopt(argc, argv, "hi:H:P:u:p:D:G:")) != -1) {
        switch (c) {
            case 'h':
                usage();
                exit(0);
            case 'i':
                interface = optarg;
                break;
        }
    }
        
    httppcap_pcap_start(interface);
	
    return 0;
}

