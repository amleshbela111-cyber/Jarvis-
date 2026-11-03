package com.example.simplecalendar

import android.os.Bundle
import android.widget.CalendarView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val calendarView = CalendarView(this)
        setContentView(calendarView)

        calendarView.setOnDateChangeListener { _, year, month, dayOfMonth ->
            val date = "$dayOfMonth/${month + 1}/$year"
            Toast.makeText(this, "Selected Date: $date", Toast.LENGTH_SHORT).show()
        }
    }
}