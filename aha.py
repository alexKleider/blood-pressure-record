#!/usr/bin/env python

# File: aha.py

"""
American Heart Association (AHA)[1]
Blood preasure criteria for hypertension

BLOOD PRESSURE CATEGORY   SYSTOLIC   &/or DIASTOLIC
-----------------------   --------   ---- ---------
NORMAL                     < 120      &     < 80
ELEVATED                  120 – 129   &     < 80
(HYPERTENSION) STAGE 1    130 – 139   or    80 – 89
(HYPERTENSION) STAGE 2     >= 140     or    >= 90
HYPERTENSIVE CRISIS        > 180     &/or   > 120

[1]
http://www.heart.org/HEARTORG/Conditions/HighBloodPressure/KnowYourNumbers/Understanding-Blood-Pressure-Readings_UCM_301764_Article.jsp#.WjW1DfZry1I
"""

import re

class AHA(object):

    """
    American Heart Association classification of hypertension.
    """

    def __init__(self):

        self.running_sys_total = 0
        self.running_dia_total = 0
        self.running_pulse_total = 0
        self.n_readings = 0

        self.categories = [
            dict(  # 0
                level = ' ',
                name = "Normal",
                expanded_name = "Normal blood pressure",
                ),
            dict(  # 1
                level = '1',
                name = "Elevated",
                expanded_name = "Elevated blood pressure",
                ),
            dict(  # 2
                level = '2',
                name = "Stage 1",
                expanded_name = "Stage 1 hypertension",
                ),
            dict(  # 3
                level = '3',
                name = "Stage 2",
                expanded_name = "Stage 2 hypertension",
                ),
            dict(  # 4
                level = '4',
                name = "Crisis",
                expanded_name = "Hypertensive Crisis!",
                ),
        ]
        
        for category in self.categories:
            category["running_sys_total"] = 0
            category["running_dia_total"] = 0
            category["running_pulse_total"] = 0
            category["count"] = 0

    def category_int(self, systolic, dia):
        """
        Returns an integer (unless there is an error!)
        coresponding to (zero based) [0] normal blood presure,
        [1]elevated blood presure, [2]stage 1 hypertension,
        [3]stage 2 hypertension, [4]hypertensive crisis.
        Because of ambiguity in the criteria, order of testing is
        important. (i.e. return the 'worse case scenario')
        """
        if systolic<120 and dia<80: return 0  # "normal"
        if 120<=systolic<130 and dia<80: return 1  #  "elevated"
        if systolic>180 or dia>120: return 4  #  "crisis"
        if systolic>=140 or dia>=90: return 3  #  "stage 2"
        if 130<=systolic<140 or 80<=dia<90: return 2  #  "stage 1"
        print("ERROR")


    def add2cat(self, cat, systolic, diastolic, pulse):
        """
        Add a single recording set of values to a specific category.
        """
        self.categories[cat]["running_sys_total"] += systolic
        self.categories[cat]["running_dia_total"] += diastolic
        self.categories[cat]["running_pulse_total"] += pulse
        self.categories[cat]["count"] += 1

    def add_reading(self, systolic, diastolic, pulse):
        """
        Add a single recording set of values to appropriage category.
        """
        self.running_sys_total += systolic
        self.running_dia_total += diastolic
        self.running_pulse_total += pulse
        self.n_readings += 1
        cat = self.category_int(systolic, diastolic)
        self.add2cat(cat, systolic, diastolic, pulse)

    def show_category_breakdown(self, with_headers=False):
        """
        Returns an array of strings showing how many readings there
        are for each category.  Categories without a reading are not
        shown. Set <with_headers> to True if want header lines as
        well.
        """
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

    def average_all_readings(self):
        """
        Returns a tuple of averages: systolic, diastolic and pulse.
        """
        return (self.running_sys_total/self.n_readings,
            self.running_dia_total/self.n_readings,
            self.running_pulse_total/self.n_readings)

test_data = (
    # systolic, diastolic, category
    (119, 79, 0),
    (120, 79, 1),
    (129, 79, 1),
    (130, 79, 2),
    (134, 71, 2),
    (139, 79, 2),
    (129, 80, 2),
    (129, 89, 2),
    (140, 89, 3),
    (139, 90, 3),
    (154, 83, 3),
    (181, 119, 4),
    (181, 120, 4),
    (179, 120, 4),
    )

def test_category_int():
    ai = AHA()
    for systolic, diastolic, category in test_data:
        res = ai.category_int(systolic, diastolic)
        if not res == category:
            print("category_int({}/{}) incorrectly returns {}, not {}"
                .format(systolic, diastolic, res, category))

        
if __name__ == "__main__":

    test_category_int()

    aha = AHA()

    aha.add_reading(116, 71, 65)
    aha.add_reading(136, 71, 65)
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
        .format(*aha.average_all_readings()[:2],
            aha.categories[aha.category_int(*aha.average_all_readings()[:2])]["expanded_name"]
                ))

