#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>

int main(int argc, char* argv[]){
  //loop over files in backup/
  //save ruid
  uid_t uid = getuid();
  //run script as root
  setuid(0);
  system("/bin/bash /home/guest/safeguard.sh");
  //return to original uid
  setuid(uid); 
}
