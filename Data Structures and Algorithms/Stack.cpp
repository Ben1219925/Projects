//Copyright 2022, Bradley Peterson, Weber State University, All rights reserved.
#include <iostream>
#include <string>
#include <cstdio>
#include <stdexcept>
using std::cout;
using std::cin;
using std::cerr;
using std::endl;
using std::string;
using std::out_of_range;
//These two base classes help the assignment compile and run without any changes.  
//Dot not modify these.  You will instead override the methods in the derived 
//classes below.
template <typename T>
class BaseStack {
public:
    BaseStack() {}                                   
    // These methods just contain filler code to help the code compile on the initial run.
        BaseStack(const unsigned int size) {}            
    // In the derived classes below, you will be overriding these with your own versions.
        BaseStack(const BaseStack& objToClone) = delete;          
    // Disables copy constructor
        BaseStack operator=(const BaseStack& objToClone) = delete; 
    // Disables copy assignment
        unsigned int size() const { return 0; }                   
    // This method will be overriden in the derived class
        void push(const T& item) {}                               
    // This method will be overriden in the derived class
        T top() const { T temp{}; return temp; }                   
    // This method will beoverriden in the derived class
        void pop() { }                                             
    // This method will beoverriden in the derived class
        void popThirdFromTop() { }                                 
    // This method will be overriden in the derived class
        void pushTwoUnderTop(const T& item) { }                   
    // This method will be overriden in the derived class
        T topThirdFromTop() const { T temp{}; return temp; }       
    // This method will be overriden in the derived class
protected:
    T* arr{ nullptr };
};
//**********************************
//Write your code below here
//**********************************
template <typename T>
class StackForCS2420 : public BaseStack<T> {
public:
    StackForCS2420(const unsigned int capacity);
    // TODO: Put your destructor and other methods here
    ~StackForCS2420();
    unsigned int size();
    void push(const T& value);
    void pop();
    T top();
    void popThirdFromTop();
    void pushTwoUnderTop(const T& value);
    T topThirdFromTop();

private:
    // TODO: Put your three data members here

    unsigned int index = 0;
    unsigned int capacity = 0;

};
template <typename T>
StackForCS2420<T>::StackForCS2420(const unsigned int capacity) {
    // TODO: Write this
    this->capacity = capacity;
    this->arr = new T[capacity];
    T temp{};
    for (unsigned int i = 0; i < capacity; i++) {
        this->arr[i] = temp;
    }

}
//TODO: Write all other methods
template <typename T>
StackForCS2420<T>::~StackForCS2420() {
    delete[] this->arr;
}

template <typename T>
unsigned int StackForCS2420<T>::size() {
    return index;
}

template <typename T>
void StackForCS2420<T>::push(const T& value) {
    if (index == capacity) {
        cout << "Error, the stack is full." << endl;
        return;
    }
    this->arr[index] = value;
    index++;
}

template <typename T>
void StackForCS2420<T>::pop() {
    if (index > 0)
        this->index--;
}

template <typename T>
T StackForCS2420<T>::top() {
    if (index == 0) {
        throw std::out_of_range("Error, the stack is empty.");
    }
       return this->arr[index - 1];
}
template <typename T>
void StackForCS2420<T>::popThirdFromTop() {
    if (index > 2) {
        this->arr[index - 2] = this->arr[index - 1];
        this->arr[index - 1] = this->arr[index];
        index--;
    }

}

template <typename T>
void StackForCS2420<T>::pushTwoUnderTop(const T& value) {
    if (index == capacity) {
        cout << "Error, the stack is full." << endl;
        return;
    }
    T temp1{};
    T temp2{};
    if (index > 2) {
        temp1 = this->arr[index - 1];
        temp2 = this->arr[index - 2];
        this->arr[index] = temp1;
        this->arr[index - 1] = temp2;
        this->arr[index - 2] = value;
        index++;
    }

}


template <typename T>
T StackForCS2420<T>::topThirdFromTop() {
    if (index < 3) {
        throw std::out_of_range("Error, the stack is empty.");
    }
    return this->arr[index - 3];
}

//Write your code above here
//**********************************
//This helps with testing, do not modify.
bool checkTest(string testName, int whatItShouldBe, int whatItIs) {
    if (whatItShouldBe == whatItIs) {
        cout << "Passed " << testName << endl;
        return true;
    }
    else {
        cout << "***Failed test " << testName << " *** " << endl << "   Output was " <<
            whatItIs << endl << "   Output should have been " << whatItShouldBe << endl;
        exit(1);
        return false;
    }
}
//This helps with testing, comment it in when ready, but do not modify the code.
bool checkTest(string testName, string whatItShouldBe, string whatItIs) {
    if (whatItShouldBe == whatItIs) {
        cout << "Passed " << testName << endl;
        return true;
    }
    else {
        if (whatItShouldBe == "") {
            cout << "***Failed test " << testName << " *** " << endl << "   Output was "
                << whatItIs << endl << "   Output should have been blank. " << endl;
        }
        else {
            cout << "***Failed test " << testName << " *** " << endl << "   Output was "
                << whatItIs << endl << "   Output should have been " << whatItShouldBe << endl;
        }
        exit(1);
        return false;
    }
}
//This helps with testing, do not modify.
bool checkTestMemory(string testName, int whatItShouldBe, int whatItIs) {
    if (whatItShouldBe == whatItIs) {
        cout << "Passed " << testName << endl;
        return true;
    }
    else {
        cout << "***Failed test " << testName << " *** " << endl << ".  ";
        cout << "You are manually managing " << whatItIs << " bytes in memory, but it should be " << whatItShouldBe << " bytes." << endl;
            exit(1);
        return false;
    }
}
//This helps with testing, do not modify.
void testStackForCS2420() {
    // Last in, first out data structure (LIFO)
    string result;
    string caughtError;
    {
        StackForCS2420<int> stack(5);
        stack.push(1);
        int data = stack.top();
        checkTest("testStackForCS2420 #1", 1, data);
        checkTest("testStackForCS2420 #2", 1, stack.size());
        stack.pop();
        stack.push(11);
        stack.push(12);
        stack.push(13);
        stack.push(14);
        stack.push(15);
        checkTest("testStackForCS2420 #3", 5, stack.size());
        checkTest("testStackForCS2420 #4", 15, stack.top());
        stack.pop();
        checkTest("testStackForCS2420 #5", 14, stack.top());
        stack.pop();
        checkTest("testStackForCS2420 #6", 13, stack.top());
        stack.pop();
        checkTest("testStackForCS2420 #7", 12, stack.top());
        stack.pop();
        checkTest("testStackForCS2420 #8", 11, stack.top());
        stack.pop();
        checkTest("testStackForCS2420 #9", 0, stack.size());
        // Now cover error handling
        try {
            result = stack.top();
        }
        catch (std::out_of_range& oor) {
            caughtError = "caught";
        }
        checkTest("testStackForCS2420 #10", "caught", caughtError);
        // Try to pop an empty stack (this isn't really a test, but it shouldn't crash or affect upcoming tests)
        stack.pop();
        try {
            result = stack.top();
        }
        catch (std::out_of_range& oor) {
            caughtError = "caught";
        }
        checkTest("testStackForCS2420 #11", "caught", caughtError);
        // Check currentSize
        checkTest("testStackForCS2420 #12", 0, stack.size());
        stack.push(12);
        stack.push(32);
        checkTest("testStackForCS2420 #13", 2, stack.size());
        // Now test filling it up
        stack.push(14);
        stack.push(53);
        stack.push(47);
        checkTest("testStackForCS2420 #14", 5, stack.size());
        // This should simply not let the 20 go in, as it is out of room.
        stack.push(20);
        // Peek at what is at the top
        checkTest("testStackForCS2420 #15", 47, stack.top());
        // Grab all the items again.
        checkTest("testStackForCS2420 #16", 47, stack.top());
        stack.pop();
        checkTest("testStackForCS2420 #17", 53, stack.top());
        stack.pop();
        checkTest("testStackForCS2420 #18", 14, stack.top());
        stack.pop();
        checkTest("testStackForCS2420 #19", 32, stack.top());
        stack.pop();
        checkTest("testStackForCS2420 #20", 12, stack.top());
        stack.pop();
        // Now do error handling again
        try {
            result = stack.top();
        }
        catch (std::out_of_range& oor) {
            caughtError = "caught";
        }
        checkTest("testStackForCS2420 #21", "caught", caughtError);
    }
    {
        // Test some strings
        StackForCS2420<string> sstack(10);
        sstack.push("pencil");
        sstack.push("pen");
        sstack.push("marker");
        checkTest("testStackForCS2420 #22", 3, sstack.size());
        // Remove pen from the stack.
        string temp = sstack.top(); // Get marker
        sstack.pop();               // Remove marker
        sstack.pop();               // Remove pen
        sstack.push(temp);          // Push marker back in
        // See if it worked 
        checkTest("testStackForCS2420 #23", "marker", sstack.top());
        sstack.pop();
        checkTest("testStackForCS2420 #24", "pencil", sstack.top());
        sstack.pop();
        checkTest("testStackForCS2420 #25", 0, sstack.size());
    }
}
//This helps with testing, do not modify.
void testStackAdditional() {
    // Last in, first out data structure (LIFO)
    int result;
    string caughtError;
    {
        // Now try popThirdFromTop()
        StackForCS2420<int> stack(10);
        stack.push(1);
        stack.push(2);
        stack.push(3);
        stack.push(4);
        stack.push(5);
        stack.popThirdFromTop();  // pops the 3
        checkTest("testStackAdditional #1", 5, stack.top());
        stack.pop();  // pops the 5
        stack.pop();  // pops the 4
        checkTest("testStackAdditional #2", 2, stack.top());
        stack.pop();  // pops the 2
        stack.pop();  // pops the 1
        // This shouldn't crash.
        stack.push(1);
        stack.push(2);
        stack.popThirdFromTop();   
        // There is no third item, so the method should not need to perform any action
            checkTest("testStackAdditional #3", 2, stack.top());  // 2 was still on the top
            // This also shouldn't crash.
        stack.pop();  // pops the 2
        stack.pop();  // pops the 1
        stack.popThirdFromTop();   
        // The stack is empty, so the method should not need to perform any action
            int result;
        try {
            result = stack.top();   
            // The top() method should either return something if it can, but here it can't, so it should throw an integer.
        }
        catch (std::out_of_range& oor) {
            caughtError = "caught";
        }
        checkTest("testStackAdditional #4", "caught", caughtError);
    }
    {
        // Now try pushTwoUnderTop()
        StackForCS2420<int> stack(10);
        stack.push(1);
        stack.push(2);
        stack.push(3);
        stack.push(4);
        stack.push(5);
        stack.pushTwoUnderTop(8); // the stack should now have 1 2 3 8 4 5
        checkTest("testStackAdditional #5", 5, stack.top());
        stack.pop();
        checkTest("testStackAdditional #6", 4, stack.top());
        stack.pop();
        checkTest("testStackAdditional #7", 8, stack.top());
        stack.pop();
        checkTest("testStackAdditional #8", 3, stack.top());
        stack.pop();
        checkTest("testStackAdditional #9", 2, stack.top());
        stack.pop();
        checkTest("testStackAdditional #10", 1, stack.top());
        try {
            result = stack.top();
        }
        catch (std::out_of_range& oor) {
            caughtError = "caught";
        }
        checkTest("testStackAdditional #11", "caught", caughtError);
        // The stack is completely empty, however, this shouldn't crash
        stack.pushTwoUnderTop(10);   
        // The stack is empty, so the method should not need to perform any action
            try {
            result = stack.top();   
        // The top() method should either return something if it can, but here it can't, so it should throw an integer.
        }
        catch (std::out_of_range& oor) {
            caughtError = "caught";
        }
        checkTest("testStackAdditional #12", "caught", caughtError);
    }
    {
        // Now try topThirdFromTop()
        StackForCS2420<int> stack(10);
        stack.push(1);
        stack.push(2);
        stack.push(3);
        stack.push(4);
        stack.push(5);
        checkTest("testStackAdditional #13", 3, stack.topThirdFromTop());
        stack.pop();
        checkTest("testStackAdditional #14", 2, stack.topThirdFromTop());
        stack.pop();
        stack.pop();
        stack.pop();
        stack.pop();
        // This shouldn't crash
        stack.push(1);
        string caught = "";
        try {
            result = stack.topThirdFromTop();   
        // The topThirdFromTop() method should either return something if it can, but here it can't, so it should throw an integer.
        }
        catch (std::out_of_range& oor) {
            caughtError = "caught";
        }
        checkTest("testStackAdditional #15", "caught", caughtError);
    }
}
void pressAnyKeyToContinue() {
    cout << "Press enter to continue...";
    //Linux and Mac users with g++ don't need this
    //But everyone else will see this message.
    cin.get();
}
int main() {
    {
        testStackForCS2420();
        pressAnyKeyToContinue();
        testStackAdditional();
        pressAnyKeyToContinue();
    }
    cout << "Shutting down the program" << endl;
    return 0;
}