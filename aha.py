#!/usr/bin/env python

# File: aha.py

"""
Blood preasure criteria for hypertension according to the American
Heart Association (AHA)[1]

BLOOD PRESSURE CATEGORY   SYSTOLIC   &/or DIASTOLIC
-----------------------   --------   ---- ---------
NORMAL                     < 120      &     < 80
ELEVATED                  120 – 129   &     < 80
(HYPERTENSION) STAGE 1    130 – 139   or    80 – 89
(HYPERTENSION) STAGE 2     >= 140     or    >= 90
HYPERTENSIVE CRISIS        > 180     &/or   >= 120

[1]
http://www.heart.org/HEARTORG/Conditions/HighBloodPressure/KnowYourNumbers/Understanding-Blood-Pressure-Readings_UCM_301764_Article.jsp#.WjW1DfZry1I
"""

import re

class AHA(object):

    """
    American Heart Association classification of hypertension.
    """

    # Reg Ex:
    line_re: str = r"""
    [SMTWF][uoehra][neduit]  # week day- discarded
    [ ]
    (?P<month>[JFMAJSOND][aepuco][nbrylgptvc])
    [ ]
    (?P<date>[\s|\d]\d)
    [ ]
    (?P<time>\d\d:\d\d)
    :\d\d  # seconds- discarded
    [ ]
    [A-Z]{3,3}  # time zone- discarded
    [ ]
    (?P<year>\d{4,4})
    [ ]
    (?P<systolic>\d{2,3})
    [/]
    (?P<diastolic>\d{2,3})
    [ ]
    (?P<pulse>\d{2,3})
    """
    line_pattern = re.compile(line_re, re.VERBOSE)

    def crisis(sys, dia):
        """>180 &/or >=120"""
        if (sys > 180) or (dia >= 120):
            return True

    def stage2(sys, dia):
        """>=140 or >=90"""
        if sys >= 140 or dia >= 90:
            return True

    def stage1(sys, dia):
        """130–139 or 80–89"""
        if ((sys >= 130 and sys < 140) or
            (dia >= 80 and dia < 90)):
            return True

    def elevated(sys, dia):
        """120–129 & <80"""
        if ((sys >= 120 and sys < 130) and 
            (dia < 80)):
            return True

    def normal(sys, dia):
        """< 120 & < 80"""
        if sys < 120 and dia < 80:
            return True

    def misc(sys, dia):
        """Catch anyting that 'falls thru'!"""
        return True

    running_sys_total = 0
    running_dia_total = 0
    running_pulse_total = 0
    n_readings = 0

    categories = [  # Order (by severity) is important.
        dict(  # 4
            level = '4',
            name = "Crisis",
            expanded_name = "Crisis level hypertension!",
            count = 0,
            f = crisis,
            ),
        dict(  # 3
            level = '3',
            name = "Stage 2",
            expanded_name = "Stage 2 hypertension",
            count = 0,
            f = stage2,
            ),
        dict(  # 2
            level = '2',
            name = "Stage 1",
            expanded_name = "Stage 1 hypertension",
            count = 0,
            f= stage1,
            ),
        dict(  # 1
            level = '1',
            name = "Elevated",
            expanded_name = "Elevated blood pressure",
            count = 0,
            f = elevated,
            ),
        dict(  # 0
            level = ' ',
            name = "Normal",
            expanded_name = "Normal blood pressure",
            count = 0,
            f = normal,
            ),
        dict(  # 5  # only to catch errors of logic.
            level = '5',
            name = "Misc",
            expanded_name = "Misc- if this appears it's an error!",
            count = 0,
            f = misc,
            ),
    ]


    def add_reading(self, systolic, diastolic, pulse):
        self.running_sys_total += systolic
        self.running_dia_total += diastolic
        self.running_pulse_total += pulse
        self.n_readings += 1
        for category in self.categories:
            if category['f'](systolic, diastolic):
                category['count'] += 1
                if category["name"] == "Misc":
                    print("Warning!!")
                return
    
    def process_line(self, line):
        match = self.line_pattern.search(line)
        if match:
            self.add_reading(
                int(match.group("systolic")),
                int(match.group("diastolic")),
                int(match.group("pulse")))

    def read_file(self, infile):
        with open(infile, 'r') as f_object:
            for line in f_object:
                self.process_line(line)


    def show_category_breakdown(self, with_headers=False):
        ret = []
        if with_headers:
            ret.append("Hypertensive   # of")
            ret.append("  Category   Readings")
            ret.append("------------ --------")
        for category in self.categories:
            if category["count"]:
                ret.append("{:>9}:   {:>4}"
                    .format(category['name'], category["count"]))
        return ret

    def average_reading(self):
        return (self.running_sys_total/self.n_readings,
            self.running_dia_total/self.n_readings,
            self.running_pulse_total/self.n_readings)


    def which_category(self, systolic, diastolic, display_item="name"):
        """ display_item can be 'name', 'expanded_name or 'level'"""
        for category in self.categories:
            if category['f'](systolic, diastolic):
                # have found the appropriate category
                return category[display_item]

        
if __name__ == "__main__":

    aha = AHA()

    aha.add_reading(116, 71, 65)
    aha.add_reading(136, 71, 65)
    aha.add_reading(236, 115, 65)
    aha.add_reading(120, 72, 65)
    aha.add_reading(162, 75, 65)
    aha.add_reading(172, 86, 65)
    aha.add_reading(172, 90, 65)
    aha.add_reading(172, 100, 65)

    for item in aha.show_category_breakdown(True):
        print(item)

    print("Average reading is {:.1f}/{:.1f} which is {}"
        .format(*aha.average_reading(),
            aha.which_category(aha.average_reading()[0],
                aha.average_reading()[1],
                display_item='level')))

    print("\nMy Readings....")
    aha = AHA()
    aha.read_file("bps.txt")

    for item in aha.show_category_breakdown(True):
        print(item)

    print("Average (of {} readings) is {:.1f}/{:.1f} which is {}"
        .format(aha.n_readings,
            *aha.average_reading()[:-1],
            aha.which_category(*aha.average_reading()[:-1],
                display_item="name")
            )
        )

