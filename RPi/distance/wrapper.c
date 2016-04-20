#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

/* A simple wrapper executable to run salt_monitor through web cgi. The wrapper executable needs to 
be setuid with owner being root.
*/

int main()
{
    setuid( 0 );
    system( "/usr/bin/python /home/nikhil/IoT/RPi/distance/salt_monitor.py" );
    return 0;
}
