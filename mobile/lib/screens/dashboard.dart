import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class DashboardScreen extends StatefulWidget {
  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  final _moodController = TextEditingController();
  String _quantumState = '';
  String _universalPulse = '';
  String _cosmicInsight = '';
  String _errorMessage = '';

  Future<void> _submitMood() async {
    final response = await http.post(
      Uri.parse('http://10.0.2.2:8000/api/mood'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'mood': _moodController.text}),
    );

    final data = jsonDecode(response.body);
    if (response.statusCode == 200 && data['status'] == 'success') {
      setState(() {
        _quantumState = data['quantum_state'];
        _universalPulse = data['universal_pulse'].toString();
        _cosmicInsight = data['cosmic_insight'];
        _errorMessage = '';
      });
    } else {
      setState(() {
        _errorMessage = data['message'] ?? 'An error occurred';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('HiveMind Dashboard'),
        backgroundColor: Color(0xFF1DA1F2),
      ),
      body: Container(
        decoration: BoxDecoration(
          image: DecorationImage(
            image: AssetImage('assets/space.jpg'),
            fit: BoxFit.cover,
          ),
        ),
        child: Padding(
          padding: EdgeInsets.all(16.0),
          child: Column(
            children: [
              TextField(
                controller: _moodController,
                decoration: InputDecoration(
                  labelText: 'How do you feel today?',
                  labelStyle: TextStyle(color: Colors.white),
                  filled: true,
                  fillColor: Colors.black54,
                ),
                style: TextStyle(color: Colors.white),
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: _submitMood,
                child: Text('Sync with the Void'),
              ),
              if (_quantumState.isNotEmpty) ...[
                SizedBox(height: 20),
                Text('Quantum State: $_quantumState', style: TextStyle(color: Colors.white)),
                Text('Universal Pulse: $_universalPulse%', style: TextStyle(color: Colors.white)),
                Text('Cosmic Insight: $_cosmicInsight', style: TextStyle(color: Colors.white)),
              ],
              if (_errorMessage.isNotEmpty)
                Text(_errorMessage, style: TextStyle(color: Colors.red)),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: () => Navigator.pushNamed(context, '/dream'),
                child: Text('Explore Your Dreams'),
              ),
              ElevatedButton(
                onPressed: () => Navigator.pushNamed(context, '/resonance'),
                child: Text('View Resonance Map'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}