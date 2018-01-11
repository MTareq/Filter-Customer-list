from argparse import ArgumentParser, RawTextHelpFormatter
from math import radians, sqrt, cos, sin, asin
from json import loads, dump
from time import strftime

EARTH_RADIUS = 6371  # KiloMeters
DESIRED_REACH = 100  # KiloMeters
DUBLIN_OFFICE = (53.339428, -6.257664)  # Degrees


def find_distance(point1, point2):
    """ Description: Function to find the distance beteween
                     two points on a sphere.
        Spec: Based on Haversine formula to calculate
              distance between two points on a sphere.
        Args:
            point1: a tuple of (Latitude , Longtitude) in degrees
            point2: a tuple of (Latitude , Longtitude) in degrees

        Returns:
            Distance: Float represinting the Distance between
                      point1 & point2 in Kilometers
    """

    lat1, lon1, lat2, lon2 = map(radians, (point1[0], point1[1],
                                           point2[0], point2[1]))
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    delta_sigma = 2 * asin(sqrt(sin(delta_lat / 2) ** 2 +
                           cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2))
    distance = EARTH_RADIUS * delta_sigma
    return distance


def within_reach(distance):
    "return True if less than or equal to DESIRED_REACH"

    return distance <= DESIRED_REACH


def main(**kwargs):
    input_file = kwargs['input_file']
    output_file = kwargs['output_file']
    verbose = kwargs['verbose']
    curated_list = []
    try:
        with open(input_file, "r") as lines:
            for n, line in enumerate(lines):
                try:
                    customer_info = loads(line)
                    customer_location = (float(customer_info.pop('latitude')),
                                         float(customer_info.pop('longitude')))
                    distance = find_distance(DUBLIN_OFFICE, customer_location)

                    if within_reach(distance):
                        curated_list.append(customer_info)
                except (ValueError, KeyError) as e:
                    if verbose:
                        print("Warning::::Bad Schema on line {} ".format(n + 1), e)
                    continue
    except FileNotFoundError:
        print("Error::::no such input file")
        return

    try:
        curated_list = sorted(curated_list, key=lambda k: k['user_id'])
    except (TypeError, KeyError) as e:
        if verbose:
            print("Warning::::Bad schema please recheck input file ", e)

    if verbose:
        print(curated_list)

    if not output_file:
        output_file = 'curated_list_' + strftime("%Y%m%d-%H%M%S")

    with open(output_file + '.json', 'w') as out_file:
        dump(curated_list, out_file)


def get_args():
    description = """
    This Script filters out customers from a customers info file,
    Based on being within {} KM from Intercom.io Dublin office ({}, {}).
    Input:
        plain text file with line seperated json objects represinting customers info,
        each json object should correspond to this schema:
           {{"latitude": String or Float, "user_id": Integer, "name": String, "longitude": String or Float}}
    Output:
        JSON file represinting the curated list of customers based on the filtering criteria,
        Sorted by 'user_id' in asscending order.
    """.format(DESIRED_REACH, DUBLIN_OFFICE[0], DUBLIN_OFFICE[1])
    parser = ArgumentParser(description=description, formatter_class=RawTextHelpFormatter)
    parser.add_argument("input_file", help="input file name")
    parser.add_argument("-v", dest="verbose", help="print output to console", action="store_true")
    parser.add_argument("-o", dest="output_file", help="output file Name")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    main(**vars(args))
