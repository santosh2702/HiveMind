import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:share/share.dart';

class DreamScreen extends StatefulWidget {
  @override
  _DreamScreenState createState() => _DreamScreenState();
}

class _DreamScreenState extends State<DreamScreen> {
  final _dreamController = TextEditingController();
  Map<String, dynamic> _dreamData = {};
  String _errorMessage = '';

  Future<void> _submitDream() async {
    final response = await http.post(
      Uri.parse('http://10.0.2.2:8000/api/dream'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'dream': _dreamController.text}),
    );

    final data = jsonDecode(response.body);
    if (response.statusCode == 200 && data['status'] == 'success') {
      setState(() {
        _dreamData = data;
        _errorMessage = '';
      });
    } else {
      setState(() {
        _errorMessage = data['message'] ?? 'An error occurred';
      });
    }
  }

  void _shareInsight() {
    if (_dreamData.isEmpty) return;
    final summary = '''
My Cosmic Insight from HiveMind:
Dream: ${_dreamData['dream']}
Tone: ${_dreamData['emotional_tone']}
Themes: ${_dreamData['themes'].join(', ')}
Fears: ${_dreamData['fears'].join(', ') ?? 'None'}
PTSD: ${_dreamData['ptsd_indicator'] ?? 'None'}
Persona: ${_dreamData['traits'].join(', ') ?? 'None'}
Description: ${_dreamData['cosmic_description'].join('; ') ?? 'None'}
Explore your cosmic self at HiveMind!
''';
    Share.share(summary);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Dream Analysis'),
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
          child: SingleChildScrollView(
            child: Column(
              children: [
                TextField(
                  controller: _dreamController,
                  decoration: InputDecoration(
                    labelText: 'Describe your dream...',
                    labelStyle: TextStyle(color: Colors.white),
                    filled: true,
                    fillColor: Colors.black54,
                  ),
                  style: TextStyle(color: Colors.white),
                  maxLines: 5,
                ),
                SizedBox(height: 20),
                ElevatedButton(
                  onPressed: _submitDream,
                  child: Text('Analyze Dream'),
                ),
                if (_dreamData.isNotEmpty) ...[
                  SizedBox(height: 20),
                  Text('Dream: ${_dreamData['dream']}', style: TextStyle(color: Colors.white)),
                  Text('Emotional Tone: ${_dreamData['emotional_tone']}', style: TextStyle(color: Colors.white)),
                  Text('Themes: ${_dreamData['themes'].join(', ')}', style: TextStyle(color: Colors.white)),
                  Text('Continuation: ${_dreamData['continuation']}', style: TextStyle(color: Colors.white)),
                  Text('Resonance Score: ${_dreamData['resonance_score']}%', style: TextStyle(color: Colors.white)),
                  Text('Vision: ${_dreamData['sensory_vision']}', style: TextStyle(color: Colors.white)),
                  Text('Feel: ${_dreamData['sensory_feel']}', style: TextStyle(color: Colors.white)),
                  Text('Sound: ${_dreamData['sensory_sound']}', style: TextStyle(color: Colors.white)),
                  Text('Fears: ${_dreamData['fears'].join(', ') ?? 'None'}', style: TextStyle(color: Colors.white)),
                  Text('PTSD: ${_dreamData['ptsd_indicator'] ?? 'None'}', style: TextStyle(color: Colors.white)),
                  Text('Coping: ${_dreamData['coping_suggestion']}', style: TextStyle(color: Colors.white)),
                  Text('Persona: ${_dreamData['traits'].join(', ') ?? 'None'}', style: TextStyle(color: Colors.white)),
                  Text('Description: ${_dreamData['cosmic_description'].join('; ') ?? 'None'}', style: TextStyle(color: Colors.white)),
                  Text('Future Echoes: ${_dreamData['future_echo']}', style: TextStyle(color: Colors.white)),
                  SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: _shareInsight,
                    child: Text('Share Cosmic Insight'),
                  ),
                ],
                if (_errorMessage.isNotEmpty)
                  Text(_errorMessage, style: TextStyle(color: Colors.red)),
              ],
            ),
          ),
        ),
      ),
    );
  }
}