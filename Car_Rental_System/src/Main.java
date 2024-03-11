import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

class Vehicle {
    private String make;
    private String model;
    private int year;
    private double rentalRate;

    public Vehicle(String make, String model, int year, double rentalRate) {
        this.make = make;
        this.model = model;
        this.year = year;
        this.rentalRate = rentalRate;
    }

    public void displayInfo() {
        System.out.println("Make: " + make);
        System.out.println("Model " + model);
        System.out.println("Year: " + year);
        System.out.println("Rental Rate: " + rentalRate);
    }

    public double getRentalRate() {
        return rentalRate;
    }

    public String getMake() {
        return make;
    }

    public String getModel() {
        return model;
    }
}

class Car extends Vehicle{

    private int numDoors;
    private boolean isConvertible;
    private String fuelType;

    public Car(String make, String model, int year, double rentalRate, int numDoors, boolean isConvertible, String fuelType) {
        super(make, model, year, rentalRate);
        this.numDoors = numDoors;
        this.isConvertible = isConvertible;
        this.fuelType = fuelType;
    }

    @Override
    public void displayInfo() {
        super.displayInfo();
        System.out.println("Number of Doors: " + numDoors);
        System.out.println("Convertible: " + isConvertible);
        System.out.println("Fuel Type: " + fuelType);
    }

}

class Motorbike extends Vehicle{

    private String bikeType;

    public Motorbike(String make, String model, int year, double rentalRate, String bikeType) {
        super(make, model, year, rentalRate);
        this.bikeType = bikeType;
    }

    @Override
    public void displayInfo() {
        super.displayInfo();
        System.out.println("Bike Type" + bikeType);
    }

}

class Truck extends Vehicle{

    private int loadCapacity;
    private boolean isFourWheelDrive;
    private String cargoType;

    public Truck(String make, String model, int year, double rentalRate, int loadCapacity, boolean isFourWheelDrive, String cargoType) {
        super(make, model, year, rentalRate);
        this.loadCapacity = loadCapacity;
        this.isFourWheelDrive = isFourWheelDrive;
        this.cargoType = cargoType;
    }

    @Override
    public void displayInfo() {
        super.displayInfo();
        System.out.println("Load Capacity: " + loadCapacity);
        System.out.println("Four wheel drive: " + isFourWheelDrive);
        System.out.println("Cargo type: " + cargoType);

    }

}

class RentalSystem {

    private List<Vehicle> availableVehicles;
    private List<Vehicle> rentedVehicles;

    public RentalSystem() {
        availableVehicles = new ArrayList<>();
        rentedVehicles = new ArrayList<>();
    }

    //to add vehicles to rental system
    public void addVehicle(Vehicle vehicle) {
        availableVehicles.add(vehicle);
    }

    public List<Vehicle> getAvailableVehicles(){
        return availableVehicles;
    }

    public List<Vehicle> getRentedVehicles(){
        return rentedVehicles;
    }

    //to rent vehicle
    public void rentVehicle(Vehicle vehicle) {
        if(availableVehicles.contains(vehicle)) {
            availableVehicles.remove(vehicle);
            rentedVehicles.add(vehicle);
        }
    }

    //to return rented vehicle
    public void returnVehicle(Vehicle vehicle) {
        if(rentedVehicles.contains(vehicle)) {
            rentedVehicles.remove(vehicle);
            availableVehicles.add(vehicle);
        }
    }

    //To display available and rented vehicles
    public void displayRentalInfo() {
        System.out.println("Available vehicles: ");
        for(Vehicle av : availableVehicles) {
            av.displayInfo();
            System.out.println();
        }

        System.out.println("Rented vehicles: ");
        for(Vehicle rv : rentedVehicles) {
            rv.displayInfo();
            System.out.println();
        }
    }

    //To calculate total rental cost
    public double calculateRentalCost(Vehicle vehicle, int rentalDuration) {
        double rentalRate = vehicle.getRentalRate();
        double totalCost = rentalRate * rentalDuration;
        return totalCost;
    }

}

public class Main {

    public static void main(String[] args) {

        //Creating scanner object to get user input
        Scanner scanner = new Scanner(System.in);
        //Creating RentalSystem object which is used to call the respective methods
        RentalSystem rentalSystem = new RentalSystem();

        Vehicle car = new Vehicle("Toyota", "Supra", 2020, 100);
        Vehicle motorbike = new Vehicle("Honda", "CXR", 2000, 50);
        Vehicle truck = new Vehicle("Ford", "F150", 2001, 200);

        rentalSystem.addVehicle(car);
        rentalSystem.addVehicle(motorbike);
        rentalSystem.addVehicle(truck);

        while (true) {
            //Options for the user
            System.out.println();
            System.out.println("===== Vehicle Rental System =====");
            System.out.println("1. Rent a Vehicle");
            System.out.println("2. Return a Vehicle");
            System.out.println("3. Display Rental Information");
            System.out.println("4. Exit");
            System.out.println();
            System.out.print("Enter your choice: ");

            int choice = scanner.nextInt();
            scanner.nextLine();

            switch (choice) {
                case 1: {
                    //Rent a vehicle
                    System.out.print("Enter the vehicle make: ");
                    String make = scanner.nextLine();
                    System.out.print("Enter the vehicle model: ");
                    String model = scanner.nextLine();

                    Vehicle selectedVehicle = null;

                    //Checks the vehicles in available vehicles
                    for(Vehicle v : rentalSystem.getAvailableVehicles()) {
                        if(v.getMake().equalsIgnoreCase(make) && v.getModel().equalsIgnoreCase(model)) {
                            selectedVehicle = v;
                        }

                    }

                    if(selectedVehicle != null) {
                        //Add the vehicle to rented vehicles
                        rentalSystem.rentVehicle(selectedVehicle);
                        System.out.print("Enter the rental duration in days: ");
                        int rentalDuration = scanner.nextInt();
                        //Calculate total rental cost
                        double rc = rentalSystem.calculateRentalCost(selectedVehicle, rentalDuration);
                        System.out.println("Successfully rented.");
                        System.out.println("Total rental Cost: " + rc);
                    }
                    else {
                        System.out.println("Matching vehicle is not available for rent.");
                    }
                    break;

                }

                case 2: {
                    //Return a vehicle
                    System.out.println("Enter the vehicle make: ");
                    String make = scanner.nextLine();
                    System.out.println("Enter the vehicle model: ");
                    String model = scanner.nextLine();

                    Vehicle selectedVehicle = null;

                    //Checks the vehicles in rented vehicles
                    for(Vehicle v : rentalSystem.getRentedVehicles()) {
                        if(v.getMake().equalsIgnoreCase(make) && v.getModel().equalsIgnoreCase(model)) {
                            selectedVehicle = v;
                        }
                    }
                    if(selectedVehicle != null) {
                        //Add to the returned vehicles
                        rentalSystem.returnVehicle(selectedVehicle);
                        System.out.println("Vehicle returned successfully.");
                    }
                    else {
                        System.out.println("Invalid return. Vehicle not rented.");
                    }
                }

                case 3: {
                    //Display Rental Information
                    rentalSystem.displayRentalInfo();
                    break;
                }

                case 4: {
                    //Exit
                    System.out.println("Thank you for using the Vehicle Rental System. Goodbye!");
                    scanner.close();
                    System.exit(0);
                }

                default:
                    System.out.println("Invalid choice. Please enter valid option...");

            }
        }

    }

}