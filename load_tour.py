import sys, os
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tourism.settings")

import django
django.setup()

from reviews.models import Tour


def save_tour_from_row(tour_row):
    tour = Tour()
    tour.id = tour_row[0]
    tour.name = tour_row[1]
    tour.save()


if __name__ == "__main__":

    if len(sys.argv) == 2:
        print ("Reading from file" + str(sys.argv[1]))
        tour_df = pd.read_csv(sys.argv[1])
        print (tour_df)

        tour_df.apply(
            save_tour_from_row,
            axis=1
        )

        print ("There are {} tour").format(Tour.objects.count())

    else:
        print ("Please, provide Tour file path")
