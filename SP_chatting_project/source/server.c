#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <pthread.h>
#include <time.h>

#define BUF_SIZE 100
#define MAX_CLNT 100
#define MAX_IP 30

void * handle_clnt(void *arg);
void send_msg(char *msg, int len);
char * serverState(int count);
void menu(char port[]);

int clnt_cnt = 0;
int clnt_socks[MAX_CLNT];
pthread_mutex_t mutex;

int main(int argc, char *argv[]) {
	int serv_sock, clnt_sock;
	struct sockaddr_in serv_adr, clnt_adr;
	int clnt_adr_len;
	pthread_t t_id;

	struct tm *t;
	time_t timer = time(NULL);
	t = localtime(&timer);

	if(argc != 2) {
		printf("Usage : %s <port>\n", argv[0]);
		exit(1);
	}

	menu(argv[1]);

	pthread_mutex_init(&mutex, NULL);
	serv_sock = socket(AF_INET, SOCK_STREAM, 0);

	memset(&serv_adr, 0, sizeof(serv_adr));
	serv_adr.sin_family = AF_INET;
	serv_adr.sin_addr.s_addr = inet_addr("10.0.2.5");
	serv_adr.sin_port = htons(atoi(argv[1]));

	if(bind(serv_sock, (struct sockaddr*)&serv_adr, sizeof(serv_adr)) == -1) {
		perror("bind error");
		exit(1);
	}

	if(listen(serv_sock, 5) == -1) {
		perror("listen error");
		exit(1);
	}

	while(1) {
		t = localtime(&timer);
		clnt_adr_len = sizeof(clnt_adr);
		clnt_sock = accept(serv_sock, (struct sockaddr*)&clnt_adr, &clnt_adr_len);

		pthread_mutex_lock(&mutex);
		clnt_socks[clnt_cnt++] = clnt_sock;
		pthread_mutex_unlock(&mutex);

		pthread_create(&t_id, NULL, handle_clnt, (void*)&clnt_sock);
		pthread_detach(t_id);
		printf("Connected client IP : %s ", inet_ntoa(clnt_adr.sin_addr));
		printf("(%d-%d-%d %d:%d)\n", t->tm_year+1900, t->tm_mon+1, t->tm_mday, t->tm_hour, t->tm_min);
		printf("chatter (%d/100)\n", clnt_cnt);
	}
	close(serv_sock);
	return 0;
}

void *handle_clnt(void *arg) {
	int clnt_sock = *((int *)arg);
	int str_len =0, i;
	char msg[BUF_SIZE];

	while((str_len=read(clnt_sock, msg, sizeof(msg))) != 0)
		send_msg(msg, str_len);

	pthread_mutex_lock(&mutex);
	for(i = 0; i < clnt_cnt; i++) {
		if(clnt_sock == clnt_socks[i]) {
			while(i++ < clnt_cnt - 1)
				clnt_socks[i] = clnt_socks[i + 1];
			break;
		}
	}
	clnt_cnt--;
	pthread_mutex_unlock(&mutex);
	close(clnt_sock);

	return NULL;
}

void send_msg(char *msg, int len) {
	int i;
	pthread_mutex_lock(&mutex);
	for(i = 0; i < clnt_cnt; i++)
		write(clnt_socks[i], msg, len);
	pthread_mutex_unlock(&mutex);
}

char * serverState(int count) {
	char *stateMsg = malloc(sizeof(char) * 20);
	strcpy(stateMsg, "None");

	if(count < 5)
		strcpy(stateMsg, "Good");
	else
		strcpy(stateMsg, "Bad");

	return stateMsg;
}

void menu(char port[]) {
	system("clear");
	printf("***** Simple char server ******\n");
	printf("server port : %s\n", port);
	printf("server state : %s\n", serverState(clnt_cnt));
	printf("max connection : %d\n", MAX_CLNT);
	printf("***          Log          ***\n\n");
}
