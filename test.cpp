#include<iostream>

int main(int argc, char **argv){
  if(atoi(argv[1])){
    std::cout<<"You have a train to catch.\n";
    return 0;
  }
  else{
    std::cout<<"Where do all these guys come from?\n";
    return 1;
  }
}
