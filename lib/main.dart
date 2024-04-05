import 'dart:math';

import 'package:flutter/material.dart';

void main() {
  runApp(RestaurantApp());
}

class RestaurantApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Restaurant Reservation',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: ReservationScreen(),
    );
  }
}

class ReservationScreen extends StatefulWidget {
  @override
  _ReservationScreenState createState() => _ReservationScreenState();
}

class _ReservationScreenState extends State<ReservationScreen> {
  final List<String> restaurantNames = [
    'Restaurant A',
    'Restaurant B',
    'Restaurant C',
    'Restaurant D',
    'Restaurant E',
    'Restaurant F',
  ];

  List<Reservation> reservations = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Restaurant Reservation'),
        actions: [
          IconButton(
            icon: Icon(Icons.list),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                    builder: (context) => MyReservations(reservations)),
              );
            },
          ),
        ],
      ),
      body: ListView(
        children: [
          ListTile(
            title: Text('Choose a Restaurant'),
          ),
          ..._buildRestaurantList(),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () async {
          final selectedRestaurant = await _showRestaurantSelectionDialog();
          if (selectedRestaurant != null) {
            final result = await Navigator.push(
              context,
              MaterialPageRoute(
                  builder: (context) =>
                      AddReservationScreen(selectedRestaurant)),
            );
            if (result != null) {
              setState(() {
                reservations.add(result);
              });
            }
          }
        },
        icon: Icon(Icons.add),
        label: Text('Add Reservation'),
      ),
    );
  }

  List<Widget> _buildRestaurantList() {
    final random = Random();
    final List<String> randomRestaurantNames = [];
    while (randomRestaurantNames.length < 3) {
      final index = random.nextInt(restaurantNames.length);
      final restaurantName = restaurantNames[index];
      if (!randomRestaurantNames.contains(restaurantName)) {
        randomRestaurantNames.add(restaurantName);
      }
    }
    return randomRestaurantNames.map((name) {
      return ListTile(
        title: Text(name),
        onTap: () {
          _navigateToAddReservationScreen(name);
        },
      );
    }).toList();
  }

  Future<void> _navigateToAddReservationScreen(String restaurantName) async {
    final result = await Navigator.push(
      context,
      MaterialPageRoute(
          builder: (context) => AddReservationScreen(restaurantName)),
    );
    if (result != null) {
      setState(() {
        reservations.add(result);
      });
    }
  }

  Future<String?> _showRestaurantSelectionDialog() async {
    return await showDialog<String>(
      context: context,
      builder: (BuildContext context) {
        return SimpleDialog(
          title: Text('Select Restaurant'),
          children: restaurantNames.map((name) {
            return SimpleDialogOption(
              onPressed: () {
                Navigator.pop(context, name);
              },
              child: Text(name),
            );
          }).toList(),
        );
      },
    );
  }
}

class AddReservationScreen extends StatefulWidget {
  final String selectedRestaurant;

  AddReservationScreen(this.selectedRestaurant);

  @override
  _AddReservationScreenState createState() => _AddReservationScreenState();
}

class _AddReservationScreenState extends State<AddReservationScreen> {
  TextEditingController nameController = TextEditingController();
  TextEditingController noteController = TextEditingController();
  TextEditingController numberOfPeopleController = TextEditingController();
  String dropdownValue = 'Veg';
  DateTime selectedDate = DateTime.now();
  TimeOfDay selectedTime = TimeOfDay.now();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Add Reservation'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Text('Restaurant: ${widget.selectedRestaurant}'),
            TextField(
              controller: nameController,
              decoration: InputDecoration(labelText: 'Name'),
            ),
            TextField(
              controller: noteController,
              decoration: InputDecoration(labelText: 'Special Requests'),
            ),
            TextField(
              controller: numberOfPeopleController,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(labelText: 'Number of People'),
            ),
            SizedBox(height: 20),
            DropdownButton<String>(
              value: dropdownValue,
              onChanged: (String? newValue) {
                setState(() {
                  dropdownValue = newValue!;
                });
              },
              items: <String>['Veg', 'Non-Veg']
                  .map<DropdownMenuItem<String>>((String value) {
                return DropdownMenuItem<String>(
                  value: value,
                  child: Text(value),
                );
              }).toList(),
            ),
            SizedBox(height: 20),
            Row(
              children: [
                ElevatedButton(
                  onPressed: () => _selectDate(context),
                  child: Text('Select Date'),
                ),
                SizedBox(width: 10),
                Text(
                    'Date: ${selectedDate.year}-${selectedDate.month}-${selectedDate.day}'),
              ],
            ),
            SizedBox(height: 10),
            Row(
              children: [
                ElevatedButton(
                  onPressed: () => _selectTime(context),
                  child: Text('Select Time'),
                ),
                SizedBox(width: 10),
                Text('Time: ${selectedTime.hour}:${selectedTime.minute}'),
              ],
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                int? numberOfPeople =
                    int.tryParse(numberOfPeopleController.text);
                if (nameController.text.isNotEmpty &&
                    numberOfPeople != null &&
                    numberOfPeople > 0) {
                  Navigator.pop(
                    context,
                    Reservation(
                      name: nameController.text,
                      note: noteController.text,
                      numberOfPeople: numberOfPeople,
                      vegOrNonVeg: dropdownValue,
                      date:
                          "${selectedDate.year}-${selectedDate.month}-${selectedDate.day}",
                      time: "${selectedTime.hour}:${selectedTime.minute}",
                      restaurant: widget.selectedRestaurant,
                    ),
                  );
                } else {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text(
                          'Invalid input. Please check your input and try again.'),
                    ),
                  );
                }
              },
              child: Padding(
                padding: const EdgeInsets.symmetric(
                    vertical: 16.0, horizontal: 32.0),
                child: Text(
                  'Save',
                  style: TextStyle(fontSize: 20.0),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _selectDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: selectedDate,
      firstDate: DateTime.now(),
      lastDate: DateTime.now().add(Duration(days: 365)), // One year ahead
    );
    if (picked != null && picked != selectedDate) {
      setState(() {
        selectedDate = picked;
      });
    }
  }

  Future<void> _selectTime(BuildContext context) async {
    final TimeOfDay? picked = await showTimePicker(
      context: context,
      initialTime: selectedTime,
    );
    if (picked != null && picked != selectedTime) {
      setState(() {
        selectedTime = picked;
      });
    }
  }
}

class Reservation {
  final String name;
  final String note;
  final int numberOfPeople;
  final String vegOrNonVeg;
  final String date;
  final String time;
  final String restaurant;

  Reservation({
    required this.name,
    required this.note,
    required this.numberOfPeople,
    required this.vegOrNonVeg,
    required this.date,
    required this.time,
    required this.restaurant,
  });
}

class MyReservations extends StatelessWidget {
  final List<Reservation> reservations;

  MyReservations(this.reservations);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('My Reservations'),
      ),
      body: ListView.builder(
        itemCount: reservations.length,
        itemBuilder: (context, index) {
          final reservation = reservations[index];
          return ListTile(
            title: Text(reservation.name),
            subtitle: Text('${reservation.date} at ${reservation.time}'),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                    builder: (context) => ReservationDetails(reservation)),
              );
            },
          );
        },
      ),
    );
  }
}

class ReservationDetails extends StatelessWidget {
  final Reservation reservation;

  ReservationDetails(this.reservation);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Reservation Details'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Name: ${reservation.name}'),
            Text('Restaurant: ${reservation.restaurant}'),
            Text('Date: ${reservation.date}'),
            Text('Time: ${reservation.time}'),
            Text('Number of People: ${reservation.numberOfPeople}'),
            Text('Special Requests: ${reservation.note}'),
            Text('Veg/Non-Veg: ${reservation.vegOrNonVeg}'),
          ],
        ),
      ),
    );
  }
}
