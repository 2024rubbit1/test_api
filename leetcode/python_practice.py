

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

