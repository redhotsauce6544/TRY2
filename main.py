#author:cameron saunders
#student id#:001479897
#wgu routing program
#Thank you for taking the time to evaluate my program!


import datetime
import csv
from truck import Truck
from hashtable import ChainingHashTable
from packages import Packages

# Load distance CSV file
with open('distance.csv') as csfile1:
    distance_csv = csv.reader(csfile1)
    distance_csv = list(distance_csv)

# Load wgu_address CSV file
with open('wgu_address.csv') as csfile2:
    wgu_address = csv.reader(csfile2)
    wgu_address = list(wgu_address)

# Load wgu_packages CSV file
with open('wgu_packages.csv') as csfile3:
    wgu_packages = csv.reader(csfile3)
    wgu_packages = list(wgu_packages)

#loading packages into the hash table
def unload_package_data(filename, package_hash_table):
    with open(filename) as package_details:
        package_info = csv.reader(package_details)
        for package_data in package_info:
            if len(package_data) >= 7:
                pID = int(package_data[0])
                paddress = package_data[1]
                pcity = package_data[2]
                pstate = package_data[3]
                pzipcode = package_data[4]
                ptarget_time = package_data[5]
                pweight = package_data[6]
                pstatus = 'at hub'

                package_obj = Packages(pID, paddress, pcity, pstate, pzipcode, ptarget_time, pweight, pstatus)
                package_hash_table.insert(pID, package_obj)

# Create Chaining_hash_table and load package data
package_hash_table = ChainingHashTable()
unload_package_data('wgu_packages.csv', package_hash_table)

#used to turn strings of addresses into a form of ID's
def extract_address(address):
    for row in wgu_address:
        if address in row[2]:
            return int(row[0])

    #locating the distance between the two addresses using their ID's
def get_distance(x_value, y_value):
    current_distance = distance_csv[x_value][y_value]
    if current_distance == '':
        current_distance = distance_csv[y_value][x_value]
    return float(current_distance)

#caculating the distance between the two addresses
def get_difference_in_distance(a, b):
    distance = distance_csv[a][b]
    if distance == '':
        distance = distance_csv[b][a]

    return float(distance)

#using the nearest neighbor algo
def delivering_the_packages(trucks, get_distance, package_hash_table, extract_address, wgu_address):
    for truck in trucks:

        #gets the package objects for the packages to assign it to a truck
        non_delivered = [package for packageID in truck.package_id if (package := package_hash_table.lookup(packageID)) is not None]
        non_delivered = list(filter(None, non_delivered))
        #clears the packages
        truck.package_id.clear()

        while len(non_delivered) > 0:
            nearest_address = 2000
            nearest_package = None

            #locates the closest package to the current area
            for package in non_delivered:

                truck_address_point = extract_address(truck.address)
                package_address_point = extract_address(package.address)

                if get_difference_in_distance(truck_address_point, package_address_point) <= nearest_address:
                    nearest_address = get_difference_in_distance(truck_address_point, package_address_point)
                    nearest_package = package

            if nearest_package is not None:

                # Append the delivered package to the truck's load
                truck.load.append(nearest_package.package_ID)
                non_delivered.remove(nearest_package)

                # Update truck's mileage before changing the address
                truck.mileage += nearest_address

                truck.address = nearest_package.address
                travel_time = datetime.timedelta(hours=nearest_address / truck.speed)
                truck.time += travel_time
                nearest_package.delivery_time = truck.time
                nearest_package.depature_time = truck.delivery_time




       #calculates the distance between the hub and updates the trucks mileage

        return_distance = get_distance(extract_address(truck.address), extract_address(truck.address))
        truck.mileage += return_distance

    # Calculate the total mileage for all trucks
    total_mileage = sum(truck.mileage for truck in trucks)

    return total_mileage


# Create Truck objects
truckone = Truck(address='4001 South 700 East', mileage=0.0, capacity=16, speed=18,
                 package_id=[1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40],
                 load=None, delivery_time=datetime.timedelta(hours=8))

trucktwo = Truck(address='4001 South 700 East', mileage=0.0, capacity=16, load=None, speed=18,
                 package_id=[3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39],
                 delivery_time=datetime.timedelta(hours=10, minutes=20))

truckthree = Truck(address='4001 South 700 East', mileage=0.0, capacity=16, load=None, speed=18,
                   package_id=[2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33],
                   delivery_time=datetime.timedelta(hours=9, minutes=4))

# Creating the Wgu Interface
#initializing starting with the trucks, the hash table,
class WGUPSInterface:
    def __init__(self, trucks, package_hash_table, get_distance, extract_address, wgu_address):
        self.trucks = trucks
        self.package_hash_table = package_hash_table
        self.get_distance = get_distance
        self.extract_address = extract_address
        self.wgu_address = wgu_address


#       #displaying menu
    def display_menu(self):
        delivering_the_packages([truckone, trucktwo, truckthree], get_distance, package_hash_table, extract_address, wgu_address)
        print("\nWGUPS Routing Program")
        print("----------------------")
        print("1. View delivery status of all packages at a specific time")
        print("2. View delivery status of a specific package at a specific time")
        print("3. View total mileage traveled by all trucks")
        print("4. Quit")

        #having users enter package ID and time
        # looking for packages. If the packages exist, it will return the package id.
        # if not, it returns "package not found"
    def view_package_status_at_time(self):
        package_id = input("Enter the package ID: ")
        
        try:
            time_str = input("Enter the time (HH:MM:SS):")

            (h, m, s) = time_str.split(":")
            user_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

        except ValueError:
            print("Invalid time format. Please use HH:MM:SS.")
            return

        package = self.package_hash_table.lookup(int(package_id))
        if package is not None:
            self.display_package_status(package, user_time)
        else:
            print(f"Package with ID {package_id} not found.")


    def view_all_package_statuses(self):
        
        try:
            time_str = input("Enter the time (HH:MM:SS):")

            (h, m, s) = time_str.split(":")
            user_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

        except ValueError:
            print("Invalid time format. Please use HH:MM:SS.")
            return
        #looking for packages. If the packages exist, it will return the package id.
        #if not, it returns "package not found"

        for package_id in range(1, 41):
            package = self.package_hash_table.lookup(int(package_id))
          
            self.display_package_status(package, user_time)

          
        #displaying the statuses of a single package at a certain time
    def display_package_status(self, package, user_time):
        current_time = user_time

        truck_address_point = self.extract_address(package.address)
        if truck_address_point is not None:
            distance_to_hub = self.get_distance(truck_address_point, 0)



            if package.delivery_time < current_time:
                status = "Delivered"
            elif package.depature_time > current_time:
                status = 'In Transit'
            else:
                status = "At Hub"

            package_details = f"Package ID: {package.package_ID}, " \
                              f"Address: {package.address}, " \
                              f"State: {package.state}, " \
                              f"City: {package.city}, " \
                              f"Zipcode: {package.zipcode}, " \
                              f"Weight: {package.weight}, " \
                              f"Status: {status}, " \
                              f"Target Delivery Time: {package.deadline}, " \
                              f"Delivery Time: {package.delivery_time if package.delivery_time else 'N/A'}"

            print(package_details)
        else:
            print("Invalid package address.")

        #Totaling the mileage traveled by all of the trucks
    def view_total_mileage(self):
        total_mileage = delivering_the_packages([truckone, trucktwo, truckthree], get_distance, package_hash_table, extract_address, wgu_address)
        print(f"\nTotal Mileage Traveled by All Trucks: {total_mileage:.2f} miles")

        #creating 3 choices for user to run
        #creates a main loop to run the program and handles the users inputs
    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                self.view_all_package_statuses()
            elif choice == '2':
                self.view_package_status_at_time()
            elif choice == '3':
                self.view_total_mileage()
            elif choice == '4':
                print("Exiting WGUPS Routing Program. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    # Create WGUPSInterface object
    wgups_interface = WGUPSInterface([truckone, trucktwo, truckthree], package_hash_table, get_distance, extract_address, wgu_address)

    # Run the interface
    wgups_interface.run()
