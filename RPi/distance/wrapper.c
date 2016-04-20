#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
    setuid( 0 );
    system( "/usr/bin/python /home/nikhil/IoT/RPi/distance/salt_monitor.py" );
    return 0;
}
