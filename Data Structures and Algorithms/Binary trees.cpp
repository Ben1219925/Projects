// Copyright 2022, Bradley Peterson, Weber State University, all rights reserved. (3/2022)

#include <iostream>
#include <string>
#include <stack>
#include <sstream>
#include <cmath>
#include <cstdio>

using std::stack;
using std::istringstream;
using std::ostringstream;
using std::string;
using std::cout;
using std::cin;
using std::cerr;
using std::endl;
using std::pow;

struct Node
{
    string data;
    Node* left{ nullptr };
    Node* right{ nullptr };
};

class TreeParser
{
public:  
    Node* root{ nullptr };
    TreeParser();
    void displayParseTree();
    void inOrderTraversal();
    void postOrderTraversal();
    void processExpression(string& expression);
    string computeAnswer();
    

protected: 
    string expression;
    unsigned int position;
private:
    stack<string> mathStack;
    double castStrToDouble(string const& s);
    string castDoubleToStr(const double d);
    void initialize();
    void inOrderTraversal(Node* p);
    void postOrderTraversal(Node* p);
    bool isDigit(char c);
    bool isOperator(char c);
    void processExpression(Node* p);
    void computeAnswer(Node* p);

};


void TreeParser::initialize() {
    expression = "";
    position = 0;
    while (!mathStack.empty()) {
        mathStack.pop();
    }
}

double TreeParser::castStrToDouble(const string& s) {
    istringstream iss(s);
    double x;
    iss >> x;
    return x;
}

string TreeParser::castDoubleToStr(const double d) {
    ostringstream oss;
    oss << d;
    return oss.str();

}

TreeParser::TreeParser() {
    initialize();
}


void TreeParser::displayParseTree() {
    cout << "The expression seen using in-order traversal: ";
    inOrderTraversal();
    cout << endl;
    cout << "The expression seen using post-order traversal: ";
    postOrderTraversal();
    cout << endl;

}

void pressEnterToContinue() {
    printf("Press Enter to continue\n");

    cin.get();

}

void TreeParser::inOrderTraversal(){
    inOrderTraversal(this->root);
}

void TreeParser::inOrderTraversal(Node* p) {
    if (p) {
        inOrderTraversal(p->left);
        cout << p->data << " ";
        inOrderTraversal(p->right);
    }
}

void TreeParser::postOrderTraversal() {
    postOrderTraversal(this->root);
}


void TreeParser::postOrderTraversal(Node* p) {
    if (p) {
        postOrderTraversal(p->left);
        postOrderTraversal(p->right);
        cout << p->data << " ";
    }
}

void TreeParser::processExpression(string& expression) {
    if (!expression.empty()) {
        this->expression = expression;
        this->position = 0;
        this->root = new Node();
        processExpression(this->root);
    }
}

void TreeParser::processExpression(Node* p) {
    string temp;
    while (position < expression.length()){
        if (expression[position] == '(') {
            p->left = new Node();
            position++;
            processExpression(p->left);
        }
        else if (isDigit(expression[position]) || expression[position] == '.') {
            while (isDigit(expression[position]) || expression[position] == '.') {
                temp += expression[position];
                position++;
            }
            p->data = temp;
            return;
        }
        else if (isOperator(expression[position])) {
            p->data = expression[position];
                p->right = new Node();
                position++;
                processExpression(p->right);
        }
        else if (expression[position] == ')') {
            position++;
            return;
        }
        else if (expression[position] == ' ') {
            position++;
        }
    }
}

string TreeParser::computeAnswer() {
    computeAnswer(this->root);
    return mathStack.top();
}

void TreeParser::computeAnswer(Node* p) {
    if (p) {
        computeAnswer(p->left);
        computeAnswer(p->right);
        if (isDigit(p->data[0])) {
            mathStack.push(p->data);
        }
        if (isOperator(p->data[0])) {
            double B = castStrToDouble(mathStack.top());
            mathStack.pop();
            double A = castStrToDouble(mathStack.top());
            mathStack.pop();
            if (p->data == "+") {
                mathStack.push(castDoubleToStr(A + B));
            }
            if (p->data == "-") {
                mathStack.push(castDoubleToStr(A - B));
            }
            if (p->data == "*") {
                mathStack.push(castDoubleToStr(A * B));
            }
            if (p->data == "/") {
                mathStack.push(castDoubleToStr(A / B));
            }if (p->data == "^") {
                mathStack.push(castDoubleToStr(pow(A,B)));
            }
        }
    }
}

bool TreeParser::isDigit(char c) {
    if (isdigit(c)) {
        return true;
    }
    return false;
}

bool TreeParser::isOperator(char c) {
    if (c == '+' || c == '-' || c == '*' || c == '/' || c == '^') {
        return true;
    }
    return false;
}

// Copyright 2022, Bradley Peterson, Weber State University, all rights reserved. (3/2022)

int main() {

    TreeParser* tp = new TreeParser;

    string expression = "(4+7)";
    tp->processExpression(expression);
    tp->displayParseTree();
    cout << "The result is: " << tp->computeAnswer() << endl; //Should display 11 as a double output

    expression = "(7-4)";
    tp->processExpression(expression);
    tp->displayParseTree();
    cout << "The result is: " << tp->computeAnswer() << endl; //Should display 3 as a double output

    expression = "(9*5)";
    tp->processExpression(expression);
    tp->displayParseTree();
    cout << "The result is: " << tp->computeAnswer() << endl; //Should display 45 as a double output

    expression = "(4^3)";
    tp->processExpression(expression);
    tp->displayParseTree();
    cout << "The result is: " << tp->computeAnswer() << endl; //Should display 64 as a double output

    expression = "((2-5)-5)";
    tp->processExpression(expression);
    tp->displayParseTree();
    cout << "The result is: " << tp->computeAnswer() << endl; //Should display -8 as a double output

    expression = "(5 * (6/2))";
    tp->processExpression(expression);
    tp->displayParseTree();
    cout << "The result is: " << tp->computeAnswer() << endl; //Should display 15 as a double output

    expression = "((6 / 3) + (8 * 2))";
    tp->processExpression(expression);
    tp->displayParseTree();
    cout << "The result is: " << tp->computeAnswer() << endl; //Should display 18 as a double output

    expression = "(543+321)";
    tp->processExpression(expression);
    tp->displayParseTree();
    cout << "The result is: " << tp->computeAnswer() << endl; //Should display 864 as a double output

    expression = "(7.5-3.25)";
    tp->processExpression(expression);
    tp->displayParseTree();
    cout << "The result is: " << tp->computeAnswer() << endl; //Should display 4.25 as a double output

    expression = "(5 + (34 - (7 * (32 / (16 * 0.5)))))";
    tp->processExpression(expression);
    tp->displayParseTree();
    cout << "The result is: " << tp->computeAnswer() << endl; //Should display 11 as a double output

    expression = "((5*(3+2))+(7*(4+6)))";
    tp->processExpression(expression);
    tp->displayParseTree();
    cout << "The result is: " << tp->computeAnswer() << endl; //Should display 95 as a double output

    expression = "(((2+3)*4)+(7+(8/2)))";
    tp->processExpression(expression);
    tp->displayParseTree();
    cout << "The result is: " << tp->computeAnswer() << endl; //Should display 31 as a double output

    expression = "(((((3+12)-7)*120)/(2+3))^3)";
    tp->processExpression(expression);
    tp->displayParseTree();
    cout << "The result is: " << tp->computeAnswer() << endl; //Should display close to 7077888 as a double output 
                                                            //NOTE, it won't be exact, it will display as scientific notation!

    expression = "(((((9+(2*(110-(30/2))))*8)+1000)/2)+(((3^4)+1)/2))";
    tp->processExpression(expression);
    tp->displayParseTree();
    cout << "The result is: " << tp->computeAnswer() << endl; //Should display close to 1337 as a double/decimal output

    pressEnterToContinue();
    return 0;
}
