import enum as python_enum


class FrequencyEnum(python_enum.Enum):
    '''Enum for the frequency of a chore'''
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
