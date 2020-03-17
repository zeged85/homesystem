package org.freedesktop.gstreamer.tutorials.tutorial_1;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import org.freedesktop.gstreamer.tutorials.tutorial_1.TcpClient;

public class Login extends AppCompatActivity {

    private TcpClient tcpClient;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);


        setButton1();

    }



    public void setButton1(){
        findViewById(R.id.login_btn).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                //IP
                EditText ip_et = (EditText) findViewById(R.id.ip_txt);
                String IP = ip_et.getText().toString();

                //PORT
                EditText port_et = (EditText)findViewById(R.id.port_txt);
                Integer PORT = Integer.parseInt(port_et.getText() .toString());



                String login_msg = "trying to login to " + IP + ":" + PORT;
                Toast.makeText(Login.this,login_msg , Toast.LENGTH_LONG).show();





                //TcpClient tcpClient = new TcpClient(IP,PORT);



                new ConnectTask().execute("");

                //sends the message to the server
                if (tcpClient != null) {
                    tcpClient.sendMessage("testing");
                }


                if (tcpClient != null) {
                    tcpClient.stopClient();
                }


//                Intent intent = new Intent(Login.this, Tutorial1.class);
//                startActivity(intent);
//

            }
        });
    }


}
