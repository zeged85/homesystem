package org.freedesktop.gstreamer.tutorials.tutorial_1;

import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

//https://github.com/CatalinPrata/funcodetuts/blob/master/AndroidTCPClient/app/src/main/java/ro/kazy/tcpclient/ClientActivity.java

public class Login extends AppCompatActivity {

    private TcpClient mTcpClient;

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


//                SingleConnection singleConnection = new SingleConnection();
//
//                singleConnection.connect();


//                new ConnectTask().execute("testing 1 2 3..."); //TODO: does this even get sent? 1 2 3..
//
//                //sends the message to the server
//                if (tcpClient != null) {
//                    tcpClient.sendMessage("testing"); //Does this?
//                }
//
//
//                if (tcpClient != null) {
//                    tcpClient.stopClient();
//                }




                new ConnectTask().execute("");




//                Intent intent = new Intent(Login.this, Controller.class);
//                startActivity(intent);
//

            }
        });
    }






    /**
     * Sends a message using a background task to avoid doing long/network operations on the UI thread
     */
    public class SendMessageTask extends AsyncTask<String, Void, Void> {

        @Override
        protected Void doInBackground(String... params) {

            // send the message
            mTcpClient.sendMessage(params[0]);

            return null;
        }

        @Override
        protected void onPostExecute(Void nothing) {
            super.onPostExecute(nothing);
            // clear the data set
            //arrayList.clear();
            // notify the adapter that the data set has changed.
            // mAdapter.notifyDataSetChanged();
        }
    }
    /**
     * Disconnects using a background task to avoid doing long/network operations on the UI thread
     */
    public class DisconnectTask extends AsyncTask<Void, Void, Void> {

        @Override
        protected Void doInBackground(Void... voids) {

            // disconnect
            mTcpClient.stopClient();
            mTcpClient = null;

            return null;
        }

        @Override
        protected void onPostExecute(Void nothing) {
            super.onPostExecute(nothing);
            // clear the data set
//                arrayList.clear();
            // notify the adapter that the data set has changed.
//                mAdapter.notifyDataSetChanged();
        }
    }



    public class ConnectTask extends AsyncTask<String, String, TcpClient> {

        @Override
        protected TcpClient doInBackground(String... message) {

            //we create a TCPClient object and
            mTcpClient = new TcpClient(new TcpClient.OnMessageReceived() {
                @Override
                //here the messageReceived method is implemented
                public void messageReceived(String message) {
                    //this method calls the onProgressUpdate
                    System.out.println("in on messageRecieved");
                    System.out.println(message);


//                    Toast.makeText(Login.this,message , Toast.LENGTH_LONG).show();

                    publishProgress(message);
                }
            });
            mTcpClient.run();

            return null;
        }

        @Override
        protected void onProgressUpdate(String... values) {
            super.onProgressUpdate(values);

            System.out.println("in on progress");
            System.out.println(values);
            System.out.println(values[0]);
            //in the arrayList we add the messaged received from server
//                arrayList.add(values[0]);
            // notify the adapter that the data set has changed. This means that new message received
            // from server was added to the list
//                mAdapter.notifyDataSetChanged();
        }
    }


}
