import 'package:flutter/material.dart';
import 'package:gyp/view/signup_page.dart';

class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack( // Use Stack for layering
        children: [
          // Background image
          Image.asset(
            'assets/gyp-background.jpg',
            fit: BoxFit.cover, // Adjust fit as needed
            width: double.infinity,
            height: double.infinity,
          ),
          // Content positioned on top
          Positioned(
           // Adjust left offset as needed (optional)
            child: Container( // Container for padding (optional)
              margin: const EdgeInsets.all(24),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  _header(context),
                  _inputField(context),
                  _forgotPassword(context),
                  _signup(context),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

 _header(context) {
    return const Column(
      children: [
       
         Text(
          "G.Y.P",
          style: TextStyle(fontSize: 40, fontWeight: FontWeight.bold),
        ),
         Text("Gym in Your Pocket",
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
         Text("Seu treino acessível a qualquer momento",
            style: TextStyle(fontSize: 14)),
      ],
    );
  }

  _inputField(context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        TextField(
          decoration: InputDecoration(
              hintText: "Usuário",
              border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(18),
                  borderSide: BorderSide.none
              ),
              fillColor: Colors.cyan.withOpacity(0.1),
              filled: true,
              prefixIcon: const Icon(Icons.person)),
        ),
        const SizedBox(height: 10),
        TextField(
          decoration: InputDecoration(
            hintText: "Senha",
            border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(18),
                borderSide: BorderSide.none),
            fillColor: const Color.fromARGB(255, 253, 253, 253).withOpacity(0.1),
            filled: true,
            prefixIcon: const Icon(Icons.password),
          ),
          obscureText: true,
        ),
        const SizedBox(height: 10),
        ElevatedButton(
          onPressed: ( ) { 
          },
          style: ElevatedButton.styleFrom(
            shape: const StadiumBorder(),
            padding: const EdgeInsets.symmetric(vertical: 16),
            backgroundColor: Colors.cyan,
          ),
          child: const Text(
            "Login",
            style: TextStyle(fontSize: 20),
          ),
        )
      ],
    );
  }

  _forgotPassword(context) {
    return TextButton(
      onPressed: () {},
      child: const Text("Esqueceu sua senha?",
        style: TextStyle(color: Colors.cyan),
      ),
    );
  }

  _signup(context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        const Text("Não possui uma conta?"),
        TextButton(
            onPressed: () {
            },
            child: const Text("Se Inscreva", style: TextStyle(color: Colors.cyan),)
        )
      ],
    );
  }
}