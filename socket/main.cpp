//main.cpp
#include "j_socket.h"
#include <stdio.h>
#include <pthread.h>
static int port=21;
j_server* ser;
void* main_listen( void* args)
{
    ser=new j_server(port);
    ser->j_listen();
}
int main()
{
    static pthread_t listen_p;
    int ret;
    ret= pthread_create( &listen_p, NULL, main_listen, NULL ); //�������������߳�id���̲߳������߳����к�������ʼ��ַ�����к����Ĳ���
    if( ret != 0 ) //�����̳߳ɹ�����0
    {
        printf("pthread_create error:error_code=%d\n",ret );
    }
    static j_client* cli;
    cli =new j_client("127.0.0.1",port);
    cli->j_send();
    return 0;
}
