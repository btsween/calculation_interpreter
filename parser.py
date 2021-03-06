class Node:

    def __init__(self,value):
        expressions = ['/', '*', '+', '-', '(', ')', '^']
        if value in expressions:
            self.identifier = 'token'
        else:
            self.identifier = 'num'
        self.value = value
        self.left = None
        self.right = None

    def set_left(self, node):
        self.left = node

    def set_right(self, node):
        self.right = node

    def get_right(self):
        return self.right

    def get_left(self):
        return self.left

    def get_type(self):
        return self.identifier

    def get_value(self):
        return self.value

    def evaluate(self, n):
        self_count = 0
        other = 0
        if(self.value in ['+','-']):
            self_count = 1
        elif(self.value in ['*','/']):
            self_count = 2
        else:
            self_count = 3
        if (n.get_value() in ['+', '-']):
            other = 1
        elif (n.get_value() in ['*', '/']):
            other = 2
        else:
            other = 3
        if(self_count > other):
            return 1
        if(self_count==other):
            return 0
        return -1

class Parser:

    def recursive_paren_check(self, given_string, paren_count):
        if len(given_string) == 0:
            return paren_count == 0
        if paren_count == 0 and given_string[0] == ')':
            return False
        if given_string[0] == '(':
            paren_count += 1
        if given_string[0] == ')':
            paren_count -= 1
        return self.recursive_paren_check(given_string[1:len(given_string)], paren_count)

    def parse_to_tree(self,expression):
        tree = AST()
        if not self.recursive_paren_check(expression, 0):
            print("error: improper parentheses")
            failed_tree = AST()
            failed_tree.add_to_tree(Node(0),None)
            return failed_tree
        tokens = ['/', '*', '+', '-', '(', ')', '^']
        num = 0
        i = 0
        while(i < len(expression)-1):
            current_num = expression[i]
            current_token = expression[i+1]
            if current_num not in tokens:
                tree.add_to_tree(Node(current_num), Node(current_token))
            i = i + 1
            num = expression[i]
        tree.add_to_tree(Node(num),None)
        return tree

    def create_subtree(self, substring):
        if(len(substring) == 0):
            return None

class AST:

    def __init__(self):
        self.head = None
        self.current = None

    def add_to_tree(self, num, token):
        if self.head == None:
            if token == None:
                self.head = num
                return
            self.current = token
            self.head = token
            token.set_left(num)
            return
        if token == None:
            self.current.set_right(num)
            return
        if self.current.evaluate(token) > 0:
            self.current.set_right(num)
            if self.head.evaluate(token) == 1:
                token.set_left(self.head)
                self.head = token
                self.current = token
                return
            else:
                flag = True
                temp_head = self.head
                self.current = self.head.get_right()
                while(flag):
                    if self.current.evaluate(token) > -1:
                        token.set_left(self.current)
                        temp_head.set_right(token)
                        self.current = token
                        flag = False
                        return
                    else:
                        temp_head = self.current
                        self.current = self.current.get_right()

        if self.current.evaluate(token) < 1:
            self.current.set_right(token)
            token.set_left(num)
            self.current = token
            return

    def print_tree(self):
        self.print_tree_helper(self.head)

    def print_tree_helper(self, node):
        if node.get_left() is None:
            return
        self.print_tree_helper(node.get_left())
        print(node.get_value())
        self.print_tree_helper(node.get_right())

    def evaluate_tree(self):
        if self.head.get_left() is None and self.head.get_right() is None:
             print(self.head.get_value())
             return
        return self.evaluate_tree_helper(self.head)

    def evaluate_tree_helper(self, node):
        if node.get_left() is None:
            print(node.get_value())
            print("left is none...")
            return node.get_value()
        left_value = self.evaluate_tree_helper(node.get_left())
        right_value = self.evaluate_tree_helper(node.get_right())
        print((left_value, right_value, node.get_value()))
        value = self.operate(left_value, right_value, node.get_value())
        print(value)
        return value


    def operate(self, v1, v2, t):
        v1 = float(v1)
        v2 = float(v2)
        if t is '+':
            return v1+v2
        if t is '-':
            return v1-v2
        if t is '*':
            return v1*v2
        if t is '/':
            return v1/v2
        if t is '^':
            return v1**v2

#Write your expression below
expression = "7*4^3-1"

#The expression is put into a tree in an order such that an algorithm can identify the order to do each operation
abstract_tree = Parser().parse_to_tree(expression)

#Expression is evaluated printing each step
result = abstract_tree.evaluate_tree()

#Print result
print(result)
