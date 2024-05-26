"""
Analysis question.
Change these default values to obtain the specified policies through value iteration.
If any question is not possible, return just the constant NOT_POSSIBLE:
```
return NOT_POSSIBLE
```
"""

NOT_POSSIBLE = None

def question2():
    """
    [Enter a description of what you did here.]
    """

    answerDiscount = 0.9
    answerNoise = 0.0

    return answerDiscount, answerNoise

def question3a():
    """
    [Enter a description of what you did here.]
    Prefer the close exit (+1), risking the cliff (-10)
    Lower discount for s shorter sight
    0 noise to risk the cliff
    low living reward so that ending is better
    """

    answerDiscount = 0.1
    answerNoise = 0.0
    answerLivingReward = -2.0

    return answerDiscount, answerNoise, answerLivingReward

def question3b():
    """
    [Enter a description of what you did here.]
    Prefer the close exit (+1), but avoiding the cliff (-10)
    low discount for short sight
    noise to avoid risk
    low living reward so that ending is better
    """

    answerDiscount = 0.1
    answerNoise = 0.1
    answerLivingReward = -1.0

    return answerDiscount, answerNoise, answerLivingReward

def question3c():
    """
    [Enter a description of what you did here.]
    Prefer the distant exit (+10), risking the cliff (-10)
    high discount for longer sight
    no noise to take risk
    low living reward to ensure ending is better
    """

    answerDiscount = 0.9
    answerNoise = 0.0
    answerLivingReward = -2.0

    return answerDiscount, answerNoise, answerLivingReward

def question3d():
    """
    [Enter a description of what you did here.]
    Prefer the distant exit (+10), avoiding the cliff (-10)
    low discount for farther sight
    noise for avoiding risk
    low living reward to ensure end
    (default case we were given)
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3e():
    """
    [Enter a description of what you did here.]
    Avoid both exits (also avoiding the cliff)
    high noise to avoid cliff
    no living reward for no end
    """

    answerDiscount = 0.9
    answerNoise = 1.0
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question6():
    """
    [Enter a description of what you did here.]
    """
    return 'NOT POSSIBLE'

if __name__ == '__main__':
    questions = [
        question2,
        question3a,
        question3b,
        question3c,
        question3d,
        question3e,
        question6,
    ]

    print('Answers to analysis questions:')
    for question in questions:
        response = question()
        print('    Question %-10s:\t%s' % (question.__name__, str(response)))
