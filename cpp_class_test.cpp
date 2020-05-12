#include <iostream>

class class_A{
  public:
    int N;
    int M;

    int give_N(){
      return N;
    }

    void set_N(const int n){
      N = n;
    }
};

class class_B{
  public:
    class_A obj;
};


int main(){
  class_B objB;
  objB.obj.set_N(4);

  return 0;
}

