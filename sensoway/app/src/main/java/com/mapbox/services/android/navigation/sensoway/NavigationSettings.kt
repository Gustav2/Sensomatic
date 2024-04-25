package com.mapbox.services.android.navigation.sensoway;
import android.annotation.SuppressLint
import android.os.Build
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity


class NavigationSettings : AppCompatActivity() {
    private lateinit var saveSettingsButton: Button
    private lateinit var usernameTextView: TextView
    @RequiresApi(Build.VERSION_CODES.N)
    @SuppressLint("MissingInflatedId", "SetTextI18n")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_navigation_settings)

        saveSettingsButton = findViewById(R.id.saveSettingsButton)
        usernameTextView = findViewById(R.id.usernameTextView)
        saveSettingsButton.setOnClickListener { sendRequest() }
    }




    @RequiresApi(Build.VERSION_CODES.N)
    fun sendRequest() {
        (application as NavigationApplication).username = usernameTextView.text.toString()
        Toast.makeText(this, "Settings saved", Toast.LENGTH_SHORT).show()

    }
}