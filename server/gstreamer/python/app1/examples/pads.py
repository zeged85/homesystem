import sys
# Gstreamer
import gi 
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, GLib

# initialize GStreamer
Gst.init(None)
# This does some things:
# 1. It initializes all internal structures
# 2. It checks what plugins are available.
# 3. It executes any command-line option intended for GStreamer

# Build pipeline
source = Gst.ElementFactory.make('souphttpsrc', 'source')
decoder = Gst.ElementFactory.make('decodebin', 'decoder')
encoder = Gst.ElementFactory.make('jpegenc', 'encoder')
avi = Gst.ElementFactory.make('avimux', 'avimux')
sink = Gst.ElementFactory.make('filesink', 'sink')


# Create empty pipeline
pipeline = Gst.Pipeline.new('test-pipeline')

if (not pipeline or not source or not decoder or not sink or not encoder or not avi):
  print('ERROR: could not init pipeline')
  sys.exit(1)

# build the pipeline
pipeline.add(source)
pipeline.add(decoder)
pipeline.add(encoder)
pipeline.add(avi)
pipeline.add(sink)

print('Added all sources')



if not source.link(decoder):
  print('ERROR: Could not link source to decoder')
  sys.exit(1)

if not decoder.link(encoder):
  print('ERROR: Could not link decoder to ' + encoder.get_property('name'))
  #sys.exit(1)

if not encoder.link(avi):
  print('ERROR: Could not link ' + encoder.get_property('name') + ' with ' + 
    avi.get_property('name'))
  sys.exit(1)

if not avi.link(sink):
  print('ERROR: Could not link ' + avi.get_property('name') + ' with ' + 
    sink.get_property('name'))

print('linked all sources')
# modify source and sink properties
#source.set_property('location', './my_movie.mp4')
#print(source.get_property('location'))
tst = """https://r2---sn-m4vox-ua8s.googlevideo.com/videoplayback?expire=1611440572&ei=XE0MYNb6MMSy1gKuoLroBA&ip=5.102.225.128&id=o-ABL3Py2cF11LPkGmR95rtyaNKuvw1ByfnR0Z582bnIU7&itag=22&source=youtube&requiressl=yes&mh=eV&mm=31%2C29&mn=sn-m4vox-ua8s%2Csn-4g5edne7&ms=au%2Crdu&mv=m&mvi=2&pl=20&initcwndbps=545000&vprv=1&mime=video%2Fmp4&ns=LuxaOK8Z-E3T4WGZaJS3AvoF&ratebypass=yes&dur=140.387&lmt=1572989225009924&mt=1611418611&fvip=2&c=WEB&txp=5532432&n=2QXaIpEZGqGgV8H&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRQIhAKaiGKyGSn1lhhKdo14mAEQwjAwczJPf4Nufpa_uAHmbAiA6Qtd_tOEsCIMQ3VcSQUtHipeHu9uG5oyrleyn25ycwA%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAID4GBxljfkGRGZXv0nk9kT7rhcvM67aDWerCXaS6fX7AiEA9IwlsN5U-Eif0o1c9OEVTB_Y3jcyx422axs4sTtpnDg%3D"""
source.set_property("is-live", True)
source.set_property("location", tst)

sink.set_property('location', './encoded_movie.avi')
print(sink.get_property('location'))

def decodebin_pad_added(element, pad):
    string = pad.query_caps(None).to_string()
    print('Found stream: %s' % string)
    if string.startswith('video/x-raw'):
        pad.link(encoder.get_static_pad('sink'))


decoder.connect("pad-added", decodebin_pad_added)

# Start playing
try:
  # start playing
  ret = pipeline.set_state(Gst.State.PLAYING)
  if ret == Gst.StateChangeReturn.FAILURE:
    print("ERROR: Unable to set the pipeline to the playing state")
  else:
    print('Pipeline started')

  # wait for EOS or error
  bus = pipeline.get_bus()
  msg = bus.timed_pop_filtered(
    Gst.CLOCK_TIME_NONE,
    Gst.MessageType.ERROR | Gst.MessageType.EOS
  )
  # Error handling
  if msg:
    t = msg.type 
    if t == Gst.MessageType.ERROR:
      err, dbg = msg.parse_error()
      print('ERROR:', msg.src.get_name(), '\n', err.message)
      if dbg:
          print('Debugging info:', dbg)
    elif t == Gst.MessageType.EOS:
      print('End-Of-Stream reached')
    print('Clean up pipeline')
    pipeline.set_state(Gst.State.NULL)
except KeyboardInterrupt:
  # Free resources and exit
  pipeline.set_state(Gst.State.NULL)
  sys.exit()       
finally:
  pipeline.set_state(Gst.State.NULL)