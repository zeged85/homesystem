package org.freedesktop.gstreamer.tutorials.tutorial_1;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import android.view.View.OnClickListener;

import android.view.SurfaceHolder;
import android.view.SurfaceView;

import org.freedesktop.gstreamer.GStreamer;

//import org.freedesktop.gstreamer.tutorials.tutorial_1.GstSingle;




public class Tutorial1 extends Activity{
//    private native void nativeInit();     // Initialize native code, build pipeline, etc
//    private native void nativeFinalize(); // Destroy pipeline and shutdown native code
//    private native void nativePlay();     // Set pipeline to PLAYING
//    private native void nativePause();    // Set pipeline to PAUSED
//    private static native boolean nativeClassInit(); // Initialize native class: cache Method IDs for callbacks
//    private native void nativeSurfaceInit(Object surface);
//    private native void nativeSurfaceFinalize();
    private long native_custom_data;      // Native code will use this to keep private data

    private boolean is_playing_desired;   // Whether the user asked to go to PLAYING

    //private native String nativeGetGStreamerInfo();
    // tutorial2

    GstSingle gstArray, gstArray2;

    // Called when the activity is first created.
    @Override
    public void onCreate(Bundle savedInstanceState)
    {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        GstSingle gstSingle = new GstSingle(this);

        GstSingle gstSingle2 = new GstSingle(this);


//        try {
//            GStreamer.init(this);
//        } catch (Exception e) {
//            Toast.makeText(this, e.getMessage(), Toast.LENGTH_LONG).show();
//            this.finish();
//            return;
//        }








//        TextView tv = (TextView)findViewById(R.id.textview_info);
//        tv.setText("Welcome to " + nativeGetGStreamerInfo() + " !");

        gstArray = gstSingle;
        gstArray2 = gstSingle2;




        ImageButton play = (ImageButton) this.findViewById(R.id.button_play);
        play.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                gstArray.is_playing_desired = true;
                gstArray.nativePlay();
            }
        });

        ImageButton play2 = (ImageButton) this.findViewById(R.id.button_play2);
        play2.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                gstArray2.is_playing_desired = true;
                gstArray2.nativePlay();
            }
        });

        ImageButton pause = (ImageButton) this.findViewById(R.id.button_stop);
        pause.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                gstArray.is_playing_desired = false;
                gstArray.nativePause();
            }
        });

        ImageButton pause2 = (ImageButton) this.findViewById(R.id.button_stop2);
        pause2.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                gstArray2.is_playing_desired = false;
                gstArray2.nativePause();
            }
        });

        SurfaceView sv = (SurfaceView) this.findViewById(R.id.surface_video);
        SurfaceHolder sh = sv.getHolder();
        sh.addCallback(gstSingle);

        SurfaceView sv2 = (SurfaceView) this.findViewById(R.id.surface_video2);
        SurfaceHolder sh2 = sv2.getHolder();
        sh2.addCallback(gstSingle2);


        if (savedInstanceState != null) {
            gstArray.is_playing_desired = savedInstanceState.getBoolean("playing");
            Log.i ("GStreamer", "Activity created. Saved state is playing:" + gstArray.is_playing_desired);

//            gstArray2.is_playing_desired = savedInstanceState.getBoolean("playing2");
//            Log.i ("GStreamer", "Activity created. Saved state is playing2:" + gstArray2.is_playing_desired);
        } else {
            gstArray.is_playing_desired = false;
            Log.i ("GStreamer", "Activity created. There is no saved state, playing: false");

//            gstArray2.is_playing_desired = false;
//            Log.i ("GStreamer", "Activity created. There is no saved state, playing2: false");
        }



        Button exit = (Button) this.findViewById(R.id.btn_exit);
        exit.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
//                is_playing_desired = false;
//                nativePause();
//                nativeFinalize();
                finish();
            }
        });

//        gstSingle.state(savedInstanceState);
//        gstSingle.enableButtons();

        // Start with disabled buttons, until native code is initialized
        this.findViewById(R.id.button_play).setEnabled(false);
        this.findViewById(R.id.button_stop).setEnabled(false);

        this.findViewById(R.id.button_play2).setEnabled(false);
        this.findViewById(R.id.button_stop2).setEnabled(false);

        gstArray.nativeInit();
        gstArray2.nativeInit();


    }

    protected void onSaveInstanceState (Bundle outState) {
        Log.d ("GStreamer", "Saving state, playing:" + gstArray.is_playing_desired);
        outState.putBoolean("playing", gstArray.is_playing_desired);

//        Log.d ("GStreamer", "Saving state, playing2:" + gstArray2.is_playing_desired);
//        outState.putBoolean("playing2", gstArray2.is_playing_desired);
    }

    //Back button listener
    @Override
    public void onBackPressed() {
        //stopThread = true;
        gstArray.nativeFinalize();
//        gstArray2.nativeFinalize();
        super.onBackPressed();
    }

    protected void onDestroy() {
        gstArray.nativeFinalize();
//        gstArray2.nativeFinalize();
        super.onDestroy();
    }






    // Called from native code. This sets the content of the TextView from the UI thread.
    private void setMessage(final String message) {
        final TextView tv = (TextView) this.findViewById(R.id.textview_message);
        runOnUiThread (new Runnable() {
            public void run() {
                tv.setText(message);
            }
        });
    }

    // Called from native code. Native code calls this once it has created its pipeline and
    // the main loop is running, so it is ready to accept commands.
    private void onGStreamerInitialized () {
        Log.i ("GStreamer", "Gst initialized. Restoring state, playing:" + gstArray.is_playing_desired);
        // Restore previous playing state
        if (gstArray.is_playing_desired) {
            gstArray.nativePlay();
        } else {
            gstArray.nativePause();
        }

        if (gstArray2.is_playing_desired) {
            gstArray2.nativePlay();
        } else {
            gstArray2.nativePause();
        }

        // Re-enable buttons, now that GStreamer is initialized
        final Activity activity = this;
        runOnUiThread(new Runnable() {
            public void run() {
                activity.findViewById(R.id.button_play).setEnabled(true);
                activity.findViewById(R.id.button_stop).setEnabled(true);
            }
        });

        runOnUiThread(new Runnable() {
            public void run() {
                activity.findViewById(R.id.button_play2).setEnabled(true);
                activity.findViewById(R.id.button_stop2).setEnabled(true);
            }
        });
    }




//    static {
//        System.loadLibrary("gstreamer_android");
//        System.loadLibrary("tutorial-1");
//        nativeClassInit();
//    }



}
