import 'package:dio/dio.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const HomePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final Dio dio = Dio();

  var result = '';
  bool isLoading = false;

  final TextEditingController textController = TextEditingController();

  modelSkincare() async {
    setState(() {
      isLoading = true;
      result = '';
    });
    final response = await dio.post('http://10.0.2.2:8000/sentimen',
        data: {'text': textController.text});

    if (response.statusCode == 200) {
      setState(() {
        isLoading = false;
        result = response.data['data'];
      });
    }
  }

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Analisis Sentimen - TIM UHUY"),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Input Text
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 15, vertical: 8),
              child: Column(
                children: [
                  const Padding(
                    padding: EdgeInsets.symmetric(horizontal: 15, vertical: 8),
                    child: Text(
                      "Masukkan teks yang ingin dianalisis",
                      style: TextStyle(fontSize: 20),
                    ),
                  ),
                  TextField(
                    controller: textController,
                    decoration: const InputDecoration(
                      border: OutlineInputBorder(),
                    ),
                    maxLines: 5,
                  ),
                ],
              ),
            ),

            // Button
            ElevatedButton(
              onPressed: () {
                modelSkincare();
                // textController.clear();
              },
              child: isLoading
                  ? const Text(
                      "Loading ....",
                      style: TextStyle(fontSize: 16),
                    )
                  : const Text(
                      "Kirim",
                      style: TextStyle(fontSize: 16),
                    ),
            ),

            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                "Hasil Sentimen : $result",
                style: const TextStyle(fontSize: 22),
              ),
            )
          ],
        ),
      ),
    );
  }
}
