import 'package:flutter/material.dart';

// Skeleton generated from Figma properties; adjust widgets manually.
class WaitingApprovalScreen extends StatelessWidget {
  const WaitingApprovalScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          child:
      Column( // Waiting Approval
        spacing: 0,
        children: [
        Column( // Container
          spacing: 24.0,
          children: [
          Row( // Pending
            spacing: 10.0,
            children: [
            Column( // verified 1
              spacing: 0,
              children: [
              Column( // loading 1
                spacing: 0,
                children: [
                SizedBox(width: 28.0, height: 28.0), // Vector,
                SizedBox(width: 28.0, height: 28.0), // Vector,
                SizedBox(width: 28.0, height: 28.0), // Vector,
                SizedBox(width: 28.0, height: 28.0), // Vector,
                SizedBox(width: 28.0, height: 28.0), // Vector,
                SizedBox(width: 28.0, height: 28.0), // Vector,
                SizedBox(width: 28.0, height: 28.0), // Vector,
                SizedBox(width: 28.0, height: 28.0), // Vector,
                ],
              ),
              SizedBox(width: 44.0, height: 44.0), // Ellipse 2282,
              ],
            ),
            ],
          ),
          Column( // Content Container
            spacing: 29.0,
            children: [
            Column( // Text Section
              spacing: 16.0,
              children: [
              Text('Awaiting Admin Approval', style: TextStyle(fontFamily: 'Roboto', fontSize: 26.0, fontWeight: FontWeight.w700, height: 32.0/26.0)), // Heading 6/Bold,
              Text('Your request is reviewed.  You will be notified by email within 24–48 hours. Please check your inbox', style: TextStyle(fontFamily: 'Roboto', fontSize: 16.0, fontWeight: FontWeight.w400, height: 22.0/16.0)), // Body L/Regular,
              ],
            ),
            Column( // Button Container
              spacing: 24.0,
              children: [
              Column( // Button Wrapper
                spacing: 24.0,
                children: [
                Column( // Button
                  spacing: 24.0,
                  children: [
                  Column( // Base button/Primary
                    spacing: 0,
                    children: [
                    SizedBox(width: None, height: None), // Button text,
                    ],
                  ),
                  ],
                ),
                ],
              ),
              ],
            ),
            ],
          ),
          ],
        ),
        Column( // 🧰/Home Indicator (iPhone)
          spacing: 0,
          children: [
          SizedBox(width: 134.0, height: 5.0), // Home Indicator,
          ],
        ),
        Column( // Link
          spacing: 0,
          children: [
          SizedBox(width: 122.0, height: 22.0), // Link text,
          ],
        ),
        Text('Create an acount', style: TextStyle(fontFamily: 'Roboto', fontSize: 16.0, fontWeight: FontWeight.w500, height: 22.0/16.0)), // Body L/Medium (Under),
        ],
      ),
        ),
      ),
    );
  }
}
