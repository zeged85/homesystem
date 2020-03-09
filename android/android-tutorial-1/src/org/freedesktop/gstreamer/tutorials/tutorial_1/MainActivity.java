package org.freedesktop.gstreamer.tutorials.tutorial_1;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        setButton1();
        setButton2();


    }

    public void setButton1(){
        findViewById(R.id.btn_main).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Toast.makeText(MainActivity.this, "this is a test", Toast.LENGTH_LONG).show();

                Intent intent = new Intent(MainActivity.this, Tutorial1.class);
                startActivity(intent);

            }
        });
    }

    public void setButton2(){
        findViewById(R.id.btn_online).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                //Toast.makeText(MainActivity.this, "this is a test", Toast.LENGTH_LONG).show();

                Intent intent = new Intent(MainActivity.this, Login.class);
                startActivity(intent);

            }
        });
    }

}
