package com.mapbox.services.android.navigation.sensoway;

// Create a class to display text on the screen

import android.annotation.SuppressLint
import android.os.Build
import android.os.Bundle
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.Request
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import com.bumptech.glide.Glide
import timber.log.Timber


class NavigationApiTest : AppCompatActivity() {
    private lateinit var mDogImageView: ImageView
    private lateinit var nextDogButton: Button
    private lateinit var usernameTextView: TextView
    @RequiresApi(Build.VERSION_CODES.N)
    @SuppressLint("MissingInflatedId", "SetTextI18n")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_navigation_api_test)

        mDogImageView = findViewById(R.id.dogImageView)
        nextDogButton = findViewById(R.id.nextDogButton)
        usernameTextView = findViewById(R.id.usernameTextView)
        nextDogButton.setOnClickListener { sendRequest() }
    }

    public var username = "admin"



    @RequiresApi(Build.VERSION_CODES.N)
    fun sendRequest() {
        val volleyQueue = Volley.newRequestQueue(this)

        // Setting the username
        // Setting the username
        (application as NavigationApplication).username = usernameTextView.text.toString()


        // url of the api through which we get random dog images
        val url = "https://dog.ceo/api/breeds/image/random"

        // since the response we get from the api is in JSON,
        // we need to use `JsonObjectRequest` for
        // parsing the request response
        val jsonObjectRequest = JsonObjectRequest(
            // we are using GET HTTP request method
            Request.Method.GET,
            // url we want to send the HTTP request to
            url,
            // this parameter is used to send a JSON object
            // to the server, since this is not required in
            // our case, we are keeping it `null`
            null,

            // lambda function for handling the case
            // when the HTTP request succeeds
            { response ->
                // get the image url from the JSON object
                val dogImageUrl = response.get("message")
                // load the image into the ImageView using Glide.
                Glide.with(this).load(dogImageUrl).into(mDogImageView)
            },

            // lambda function for handling the
            // case when the HTTP request fails
            { error ->
                // make a Toast telling the user
                // that something went wrong
                Toast.makeText(this, "Some error occurred! Cannot fetch dog image", Toast.LENGTH_LONG).show()
                // log the error message in the error stream
                Timber.tag("MainActivity").e("loadDogImage error: " + error.localizedMessage)
            }
        )

        // add the json request object created
        // above to the Volley request queue
        volleyQueue.add(jsonObjectRequest)



    }
}