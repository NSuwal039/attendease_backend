PERIODS_CHOICES = [
        (1, 'First'),
        (2, 'Second'),
        (3, 'Third'),
        (4, 'Fourth'),
    ]
    
SHIFT_CHOICES = [
        ('Day', 'Day'),
        ('Mor', 'Morning')
    ]

SEMESTER_CHOICES = [(i,i) for i in range(1,9)]

DAYS_CHOICES = [
        ('SUN', 'Sunday'),
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
    ]
    
TYPE_CHOICES = [
        ('Lec', 'Lecture'),
        ('Pra', 'Practical')
    ]
    
GROUP_CHOICES = [
        ('A', 'Group A'),
        ('B', 'Group B'),
        ('-', 'Both')
    ]

ATTENDANCE_CHOICES = (
        ('P','Present'),
        ('A','Absent'),
        ('L','Leave'),
    )

CATEGORY_CHOICES = [
    ('Not', 'Notices'),
    ('Hol', 'Holiday')
]