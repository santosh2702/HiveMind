import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:fl_chart/fl_chart.dart';

class ResonanceScreen extends StatefulWidget {
  @override
  _ResonanceScreenState createState() => _ResonanceScreenState();
}

class _ResonanceScreenState extends State<ResonanceScreen> {
  Map<String, dynamic> _mapData = {};
  String _errorMessage = '';

  @override
  void initState() {
    super.initState();
    _fetchResonanceData();
  }

  Future<void> _fetchResonanceData() async {
    final response = await http.get(
      Uri.parse('http://10.0.2.2:8000/api/resonance'),
      headers: {'Content-Type': 'application/json'},
    );

    final data = jsonDecode(response.body);
    if (response.statusCode == 200 && data['status'] == 'success') {
      setState(() {
        _mapData = data['map_data'];
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
        title: Text('Cosmic Resonance Map'),
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
              Text(
                'Your moods and dreams form a galactic tapestry.',
                style: TextStyle(color: Colors.white),
                textAlign: TextAlign.center,
              ),
              SizedBox(height: 20),
              if (_mapData.isNotEmpty)
                Expanded(
                  child: ScatterChart(
                    ScatterChartData(
                      scatterSpots: [
                        ..._mapData['moods'].map((m) => ScatterSpot(
                              m['x'],
                              m['y'],
                              color: m['color'] == 'blue'
                                  ? Colors.blue
                                  : m['color'] == 'red'
                                      ? Colors.red
                                      : Colors.white,
                              radius: 5,
                            )),
                        ..._mapData['dreams'].map((d) => ScatterSpot(
                              d['x'],
                              d['y'],
                              color: Color(0xFF1DA1F2).withOpacity(0.5),
                              radius: d['size'],
                            )),
                        ..._mapData['community'].map((c) => ScatterSpot(
                              c['x'],
                              c['y'],
                              color: Colors.white.withOpacity(0.2),
                              radius: c['size'],
                            )),
                      ],
                      titlesData: FlTitlesData(show: false),
                      borderData: FlBorderData(show: false),
                      gridData: FlGridData(show: false),
                    ),
                  ),
                ),
              if (_errorMessage.isNotEmpty)
                Text(_errorMessage, style: TextStyle(color: Colors.red)),
              if (_mapData.isEmpty && _errorMessage.isEmpty)
                Text('No data available. Add moods and dreams.', style: TextStyle(color: Colors.white)),
            ],
          ),
        ),
      ),
    );
  }
}