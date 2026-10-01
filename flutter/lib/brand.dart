import 'package:flutter/material.dart';

/// ICDESK brand palette.
///
/// Mirrors `brand/tokens.css` (source of truth). Use these constants instead
/// of hardcoding hex values in widgets.
///
/// Roles: black is the base, gold is the highlight, blue is only a
/// connection accent. Status colors are separate so gold is never read as an
/// alert.
class IcBrand {
  IcBrand._();

  // Brand colors
  static const Color richBlack = Color(0xFF0D0D0D); // --cx-richblack
  static const Color gold = Color(0xFFC5A059); // --cx-gold
  static const Color goldLight = Color(0xFFE8CE94); // --cx-goldlight
  static const Color techBlue = Color(0xFF00F0FF); // --cx-techblue
  static const Color text = Color(0xFFF2F2F2); // --cx-text

  // Status (never use gold for these)
  static const Color ok = Color(0xFF22C55E); // --cx-ok
  static const Color warn = Color(0xFFEAB308); // --cx-warn
  static const Color offline = Color(0xFFEF4444); // --cx-offline

  // Logo gradient
  static const Color goldGradStart = Color(0xFFEBD7A6); // --cx-gold-grad-1
  static const Color goldGradEnd = Color(0xFF8A6A32); // --cx-gold-grad-3
  static const LinearGradient goldGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [goldGradStart, gold, goldGradEnd],
  );

  // Derived surfaces (dark UI)
  static const Color surface = Color(0xFF161616); // --cx-surface
  static const Color surface2 = Color(0xFF1F1F1F); // --cx-surface-2
  static const Color hover = Color(0xFF262626); // --cx-hover

  /// Gold for text/links on light backgrounds (contrast ≥ 4.5:1 on white).
  static const Color goldDeep = goldGradEnd; // --cx-gold-deep
}
