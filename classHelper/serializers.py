from rest_framework import serializers
from django.contrib.auth.models import User
from classHelper.models import ClassUser, ProblemSet, Problem, Solution

class ClassUserSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(source = 'user.username')
    email = serializers.CharField(source = 'user.email')
    password = serializers.CharField(source = 'user.password')
    solutions = serializers.HyperlinkedRelatedField(many = True, view_name = 'solution-detail',read_only = True)
    problemSets = serializers.HyperlinkedRelatedField(many = True, view_name = 'problemset-detail', read_only = True)

    def validate_role(self, value):
        if value == 'a':
            raise serializers.ValidationError('The Role isn\'t Exist!')
        return value

    def create(self, attrs):
        userDict = attrs['user']
        user = User.objects.create_user(username=userDict['username'], email= userDict['email'], password=userDict['password'])
        role = attrs.get('role', 's')
        return ClassUser.objects.create(user=user,role=role)

    def update(self, instance, attrs):
        #Suppose User is ReadOnly
        #user = User.objects.create_user(username=attrs.get('user.username'),
        #email= attrs.get('user.email'), password=attrs.get('user.password'))
        instance.role = attrs.get('role', instance.role)
        instance.save()
        return instance
    class Meta:
        model = ClassUser
        fields = ('username', 'email', 'role', 'password', 'problemSets', 'solutions')

class ProblemSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.ReadOnlyField(source = 'problemSet.problemSetDesc')
    code = serializers.CharField(source = 'problemSet.problemSetCode')

    class Meta:
        model = Problem
        fields = ('code', 'title', 'problemDesc', 'problemSelect',)

class ProblemSetSerializer(serializers.HyperlinkedModelSerializer):
    problems = serializers.HyperlinkedRelatedField(many = True, view_name = 'problem-detail', read_only = True)
    username = serializers.ReadOnlyField(source = 'creater.user.username')
    solutions = serializers.HyperlinkedRelatedField(many = True, view_name = 'solution-detail', read_only = True)

    class Meta:
        model = ProblemSet
        fields = ('problemSetCode', 'problemSetDesc', 'problemsAns', 'username', 'problems', 'solutions',)


class SolutionSerializer(serializers.HyperlinkedModelSerializer):
    solver = serializers.ReadOnlyField(source = 'solver.user.username')
    code = serializers.CharField(source = 'problems.problemSetCode')

    class Meta:
        model = Solution
        fields = ('code','solver','ans',)

    #def create(self, attrs):
    #    print(attrs)
    #    print()
    #    obj = ProblemSet.objects.get(problemSetCode = attrs['problemSet']['problemSetCode'])
    #    print('2')
    #    return Solution.objects.create(solver = attrs['solver'], problems = obj, ans = attrs['ans'])
