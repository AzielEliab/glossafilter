import 'package:flutter/material.dart';

/// Gold accent. Light and dark follow the system. No analytics.
const Color kGold = Color(0xFFC9A227);
const Color kGoldInk = Color(0xFF1A1408);
const Color kPaper = Color(0xFFF6F3EA);
const Color kInk = Color(0xFF1C1914);
const Color kMatteBlack = Color(0xFF12110E);
const Color kSurface = Color(0xFF1C1B17);
const Color kIvory = Color(0xFFF4EFE6);

ThemeData buildAppTheme({Brightness brightness = Brightness.light}) {
  final dark = brightness == Brightness.dark;
  final scheme = ColorScheme(
    brightness: brightness,
    primary: kGold,
    onPrimary: kGoldInk,
    secondary: kGold,
    onSecondary: kGoldInk,
    surface: dark ? kSurface : Colors.white,
    onSurface: dark ? kIvory : kInk,
    error: const Color(0xFF8D2E28),
    onError: Colors.white,
  );
  return ThemeData(
    useMaterial3: true,
    brightness: brightness,
    colorScheme: scheme,
    scaffoldBackgroundColor: dark ? kMatteBlack : kPaper,
    appBarTheme: AppBarTheme(
      backgroundColor: dark ? kMatteBlack : kPaper,
      foregroundColor: dark ? kIvory : kInk,
      elevation: 0,
      centerTitle: false,
    ),
    cardTheme: CardThemeData(
      color: dark ? kSurface : Colors.white,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: const BorderSide(color: Color(0x59C9A227)),
      ),
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: dark ? const Color(0xFF14130F) : Colors.white,
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(10),
        borderSide: const BorderSide(color: kGold, width: 2),
      ),
    ),
    segmentedButtonTheme: SegmentedButtonThemeData(
      style: ButtonStyle(
        foregroundColor: WidgetStateProperty.resolveWith((s) {
          return s.contains(WidgetState.selected) ? kGoldInk : scheme.onSurface;
        }),
        backgroundColor: WidgetStateProperty.resolveWith((s) {
          return s.contains(WidgetState.selected) ? kGold : scheme.surface;
        }),
      ),
    ),
  );
}
