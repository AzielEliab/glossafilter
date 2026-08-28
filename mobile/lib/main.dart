import 'dart:convert';

import 'package:crypto/crypto.dart';
import 'package:flutter/material.dart';

import 'theme.dart';

void main() {
  runApp(const GlossaApp());
}

class GlossaApp extends StatelessWidget {
  const GlossaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Glossa Filter',
      debugShowCheckedModeBanner: false,
      theme: buildAppTheme(),
      home: const FilterPage(),
    );
  }
}

class Pack {
  const Pack(this.id, this.label, this.glossary, this.variants, this.prop, this.blurb);
  final String id;
  final String label;
  final Map<String, String> glossary;
  final Map<String, List<String>> variants;
  final String prop;
  final String blurb;
}

const packs = [
  Pack(
    'en-plain',
    'English (plain)',
    {
      'package': 'package',
      'release': 'ships',
      'filter': 'filter',
      'tool': 'tool',
      'interface': 'interface',
      'binds': 'binds',
      'bind': 'binds',
      'loopback': 'loopback',
    },
    {
      'release': ['ships', 'puts out', 'sends out'],
      'binds': ['binds', 'hooks to', 'listens on'],
    },
    '{subject} {rel} {object}.',
    '{action} {interface}.',
  ),
  Pack(
    'en-formal',
    'English (formal)',
    {
      'package': 'package',
      'release': 'issues',
      'filter': 'filter',
      'tool': 'instrument',
      'interface': 'interface',
      'binds': 'attaches',
      'bind': 'attaches',
      'loopback': 'loopback interface',
    },
    {
      'release': ['issues', 'disseminates', 'promulgates'],
      'binds': ['attaches', 'associates', 'connects'],
    },
    '{subject} {rel} {object}.',
    '{action} {interface}.',
  ),
  Pack(
    'es',
    'Español',
    {
      'package': 'paquete',
      'release': 'publica',
      'filter': 'filtro',
      'tool': 'herramienta',
      'interface': 'interfaz',
      'binds': 'enlaza',
      'bind': 'enlaza',
      'loopback': 'bucle local',
    },
    {
      'release': ['publica', 'emite', 'expide'],
      'binds': ['enlaza', 'vincula', 'asocia'],
    },
    '{subject} {rel} {object}.',
    '{action} {interface}.',
  ),
];

int pickVariant(String digest, String peer, String lemma, int n) {
  if (n <= 0) return 0;
  final h = sha256.convert(utf8.encode('$digest|$peer|$lemma')).bytes;
  var v = 0;
  for (var i = 0; i < 8; i++) {
    v = (v << 8) + h[i];
  }
  return v % n;
}

String surface(String text, Pack pack, String digest) {
  return text.split(' ').map((token) {
    final lemma = token.toLowerCase().replaceAll(RegExp(r'[^a-z0-9_-]'), '');
    if (pack.variants.containsKey(lemma)) {
      final list = pack.variants[lemma]!;
      return list[pickVariant(digest, pack.id, lemma, list.length)];
    }
    if (pack.glossary.containsKey(lemma)) return pack.glossary[lemma]!;
    return token;
  }).join(' ');
}

class FilterPage extends StatefulWidget {
  const FilterPage({super.key});

  @override
  State<FilterPage> createState() => _FilterPageState();
}

class _FilterPageState extends State<FilterPage> {
  final _subject = TextEditingController(text: 'package');
  final _rel = TextEditingController(text: 'release');
  final _object = TextEditingController(text: 'filter');
  final _action = TextEditingController(text: 'binds');
  final _interface = TextEditingController(text: 'loopback');
  String _channel = 'tooling';
  Map<String, String>? _peers;
  String? _digest;

  @override
  void dispose() {
    _subject.dispose();
    _rel.dispose();
    _object.dispose();
    _action.dispose();
    _interface.dispose();
    super.dispose();
  }

  void _render() {
    final intent = {
      'channel': _channel,
      'propositions': [
        {'object': _object.text, 'rel': _rel.text, 'subject': _subject.text},
      ],
      'slots': {'action': _action.text, 'interface': _interface.text},
    };
    final canonical = jsonEncode(intent);
    final digest = sha256.convert(utf8.encode(canonical)).toString();
    final out = <String, String>{};
    for (final pack in packs) {
      final sub = surface(_subject.text, pack, digest);
      final rel = surface(_rel.text, pack, digest);
      final obj = surface(_object.text, pack, digest);
      final act = surface(_action.text, pack, digest);
      final iface = surface(_interface.text, pack, digest);
      final prop = pack.prop
          .replaceAll('{subject}', sub)
          .replaceAll('{rel}', rel)
          .replaceAll('{object}', obj);
      final blurb = pack.blurb.replaceAll('{action}', act).replaceAll('{interface}', iface);
      out[pack.id] = '$prop\n$blurb';
    }
    setState(() {
      _digest = digest;
      _peers = out;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Glossa Filter')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const Text(
            'Human opinion remains human, and tools remain tools.',
            style: TextStyle(color: kGold, fontStyle: FontStyle.italic),
          ),
          const SizedBox(height: 8),
          const Text(
            'Mediation, not concealment. No canonical language. Peers are equal. '
            'Not a live translator. Not identity masking.',
          ),
          const SizedBox(height: 16),
          SegmentedButton<String>(
            segments: const [
              ButtonSegment(value: 'tooling', label: Text('tooling')),
              ButtonSegment(value: 'civic', label: Text('civic')),
            ],
            selected: {_channel},
            onSelectionChanged: (s) => setState(() => _channel = s.first),
          ),
          const SizedBox(height: 12),
          TextField(controller: _subject, decoration: const InputDecoration(labelText: 'subject')),
          const SizedBox(height: 8),
          TextField(controller: _rel, decoration: const InputDecoration(labelText: 'rel')),
          const SizedBox(height: 8),
          TextField(controller: _object, decoration: const InputDecoration(labelText: 'object')),
          const SizedBox(height: 8),
          TextField(controller: _action, decoration: const InputDecoration(labelText: 'slot: action')),
          const SizedBox(height: 8),
          TextField(controller: _interface, decoration: const InputDecoration(labelText: 'slot: interface')),
          const SizedBox(height: 12),
          FilledButton(onPressed: _render, child: const Text('Render peers')),
          if (_digest != null) ...[
            const SizedBox(height: 8),
            Text('intent digest ${_digest!.substring(0, 16)}…  (content-derived, not author-derived)',
                style: const TextStyle(fontFamily: 'monospace', fontSize: 12, color: kGoldDim)),
            const SizedBox(height: 12),
            for (final pack in packs)
              Card(
                margin: const EdgeInsets.only(bottom: 10),
                child: Padding(
                  padding: const EdgeInsets.all(12),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('${pack.id}  ·  ${pack.label}  ·  peer (not primary)',
                          style: const TextStyle(color: kGold)),
                      const SizedBox(height: 6),
                      Text(_peers![pack.id] ?? ''),
                    ],
                  ),
                ),
              ),
          ],
        ],
      ),
    );
  }
}
