class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        if x<0:
            return False
        x_copy = x
        reversed_num = 0
        while x_copy > 0:
            reversed_num = reversed_num + (x_copy % 10)*10
            x_copy = x_copy // 10
        return reversed_num == x

