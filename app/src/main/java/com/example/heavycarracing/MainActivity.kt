package com.example.heavycarracing

import android.os.Bundle
import android.widget.FrameLayout
import android.widget.ImageView
import androidx.appcompat.app.AppCompatActivity
import android.view.View

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val container = FrameLayout(this)
        val car = ImageView(this)
        car.setImageResource(android.R.drawable.ic_menu_directions)
        val params = FrameLayout.LayoutParams(200, 200)
        params.leftMargin = 100
        params.topMargin = 500
        car.layoutParams = params
        container.addView(car)
        setContentView(container)
        container.setOnClickListener { 
            car.animate().translationXBy(100f).setDuration(100).start()
        }
    }
}