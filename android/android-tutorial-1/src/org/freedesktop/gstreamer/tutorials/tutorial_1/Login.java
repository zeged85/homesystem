package org.freedesktop.gstreamer.tutorials.tutorial_1;

import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.Toast;

import java.io.IOException;

//https://github.com/CatalinPrata/funcodetuts/blob/master/AndroidTCPClient/app/src/main/java/ro/kazy/tcpclient/ClientActivity.java

public class Login extends AppCompatActivity {

    private TcpClient mTcpClient;
    private String IP;
    private Integer PORT;
    private ProgressBar progressBar;
    private AsyncTask timer;
    private ProgressBar progressBar;

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
                IP = ip_et.getText().toString();

                //PORT
                EditText port_et = (EditText)findViewById(R.id.port_txt);
                PORT = Integer.parseInt(port_et.getText() .toString());



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


                //this is not how u start two threads
//                new CountdownTask().execute();
//                new ConnectTask().execute("");


                //this is the way

                new ConnectTask().executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
                timer = new CountdownTask().executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);


                progressBar = (ProgressBar)findViewById(R.id.progressBar);
                //progressBar.setVisibility(View.VISIBLE);
                showProgressbar();


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
            try {
                mTcpClient.stopClient();
            } catch (IOException e) {
                System.out.println("DisconnectTask Exception");
                //progressBar.setVisibility(View.INVISIBLE);
                hideProgressbar();
                e.printStackTrace();
            }
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

//            progressBar.setVisibility(View.INVISIBLE);
            hideProgressbar();
        }
    }



    public class ConnectTask extends AsyncTask<String, String, TcpClient> {

        @Override
        protected TcpClient doInBackground(String... message) {

            //we create a TCPClient object and
            mTcpClient = new TcpClient(IP, PORT, new TcpClient.OnMessageReceived() {
                @Override
                //here the messageReceived method is implemented
                public void messageReceived(String message) {
                    //this method calls the onProgressUpdate
                    System.out.println("in on messageRecieved");
                    System.out.println(message);

                    if (message.compareTo("server found!")==0){
                        //progressBar.setVisibility(View.INVISIBLE);
                        //TODO: move to onProgressUPdate
                        // stop timer

                       // timer.cancel(true);


                        System.out.println("detected the change in status");
                    }

//                    Toast.makeText(Login.this,message , Toast.LENGTH_LONG).show();

                    publishProgress(message);
                }



//                @Override
//                //here the statusReceived method is implemented
//                public void statusReceived(String status) {
//                    //this method calls the onProgressUpdate
//                    System.out.println("in on statusRecieved");
//                    System.out.println(status);
//
//
////                    Toast.makeText(Login.this,message , Toast.LENGTH_LONG).show();
//
//                    publishProgress(status);
//                }

            }, new TcpClient.OnStatusReceived() {
                @Override
                public void statusReceived(String status) {
                    //this method calls the onProgressUpdate
                    System.out.println("in on statusRecieved");
                    System.out.println(status);


//                    Toast.makeText(Login.this,message , Toast.LENGTH_LONG).show();


                    //if status == ok


                    timer.cancel(true);
//                    cancel(CountdownTask);
//                    CountdownTask. cancel
                    hideProgressbar();

                    publishProgress(status); //TODO: what is this?

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

            if (values[0].compareTo("server found!")==0){
                System.out.println("finally the place to update change");

                timer.cancel(true);
                progressBar.setVisibility(View.INVISIBLE);

            }

            //in the arrayList we add the messaged received from server
//                arrayList.add(values[0]);
            // notify the adapter that the data set has changed. This means that new message received
            // from server was added to the list
//                mAdapter.notifyDataSetChanged();
        }
    }

    public class CountdownTask extends AsyncTask<Void, Void, Void>{

        @Override
        protected Void doInBackground(Void... voids) {

            System.out.println("starting countdown");

            try {
                Thread.sleep(5000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }


            return null;
        }


        @Override
        protected void onPostExecute(Void v){
            String login_msg = "timeout";
            Toast.makeText(Login.this,login_msg , Toast.LENGTH_LONG).show();
            System.out.println("countdown over");
            new DisconnectTask().execute();

        }

    }

    public void hideProgressbar(){
        progressBar.setVisibility(View.INVISIBLE);

    }

    public void showProgressbar(){
        progressBar.setVisibility(View.VISIBLE);
    }

}
