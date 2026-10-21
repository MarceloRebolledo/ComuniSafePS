import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:comunisafe/widgets/app_button.dart';
import 'package:comunisafe/providers/theme_provider.dart';

void main() {
  testWidgets('AppButton renderiza el título correctamente',
      (WidgetTester tester) async {
    bool wasPressed = false;

    await tester.pumpWidget(
      ChangeNotifierProvider(
        create: (_) => ThemeProvider(),
        child: MaterialApp(
          home: Scaffold(
            body: AppButton(
              title: 'Prueba de Botón',
              onPressed: () {
                wasPressed = true;
              },
            ),
          ),
        ),
      ),
    );

    expect(find.text('Prueba de Botón'), findsOneWidget);

    await tester.tap(find.text('Prueba de Botón'));
    expect(wasPressed, isTrue);
  });
}
