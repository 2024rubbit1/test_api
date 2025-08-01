

class PythonPractice:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def two_sum(self, nums, target):
        """
        两数相加之和等于target，返回两数的下标
        """
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]

    def isPalindrome(self, x: int) -> bool:
        """
        判断一个整数是否是回文数
        回文数是指正序（从左向右）和倒序（从右向左）读都是一样的整数。
        """
        if x < 0:
            return False
        if x == 0:
            return True
        if x % 10 == 0:
            return False
        num = 0
        while x > num:
            num = num * 10 + x % 10
            x = x // 10
        return x == num or x == num // 10

