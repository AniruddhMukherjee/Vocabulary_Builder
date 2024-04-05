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
  List<Reservation> reservations = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Restaurant Reservation'),
      ),
      body: ListView.builder(
        itemCount: reservations.length,
        itemBuilder: (BuildContext context, int index) {
          return ListTile(
            title: Text(reservations[index].name),
            subtitle: Text(
                'Date: ${reservations[index].date}, Time: ${reservations[index].time}, ${reservations[index].numberOfPeople} people, ${reservations[index].vegOrNonVeg}, Special Requests: ${reservations[index].note}'),
            trailing: IconButton(
              icon: Icon(Icons.delete),
              onPressed: () {
                setState(() {
                  reservations.removeAt(index);
                });
              },
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          final result = await Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => AddReservationScreen()),
          );
          if (result != null) {
            setState(() {
              reservations.add(result);
            });
          }
        },
        child: Icon(Icons.add),
      ),
    );
  }
}

class AddReservationScreen extends StatefulWidget {
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
                if (nameController.text.isNotEmpty &&
                    numberOfPeopleController.text.isNotEmpty) {
                  Navigator.pop(
                    context,
                    Reservation(
                      name: nameController.text,
                      note: noteController.text,
                      numberOfPeople: int.parse(numberOfPeopleController.text),
                      vegOrNonVeg: dropdownValue,
                      date:
                          "${selectedDate.year}-${selectedDate.month}-${selectedDate.day}",
                      time: "${selectedTime.hour}:${selectedTime.minute}",
                    ),
                  );
                }
              },
              child: Text('Save'),
            ),
          ],
        ),
      ),
    );
  }
}

class Reservation {
  final String name;
  final String note;
  final int numberOfPeople;
  final String vegOrNonVeg;
  final String date;
  final String time;

  Reservation({
    required this.name,
    required this.note,
    required this.numberOfPeople,
    required this.vegOrNonVeg,
    required this.date,
    required this.time,
  });
}
