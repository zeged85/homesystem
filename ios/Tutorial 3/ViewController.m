#import "ViewController.h"
#import "GStreamerBackend.h"
#import <UIKit/UIKit.h>

@interface ViewController () {
    GStreamerBackend *gst_backend;
    GStreamerBackend *gst_backend2;
    int media_width;
    int media_height;
}

@end

@implementation ViewController

/*
 * Methods from UIViewController
 */

- (void)viewDidLoad
{
    [super viewDidLoad];

    play_button.enabled = FALSE;
    pause_button.enabled = FALSE;

    /* Make these constant for now, later tutorials will change them */
    media_width = 320;
    media_height = 240;
    
    NSString* text1 = @"videotestsrc pattern = 1 ! glimagesink";
    NSString* text2 = @"videotestsrc pattern = 0 ! glimagesink";

    gst_backend = [[GStreamerBackend alloc] init:self videoView:video_view uri:text1];
    gst_backend2 = [[GStreamerBackend alloc] init:self videoView:video_view2 uri:text2];
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

/* Called when the Play button is pressed */
-(IBAction) play:(id)sender
{
    [gst_backend play];
    [gst_backend2 play];
}

/* Called when the Pause button is pressed */
-(IBAction) pause:(id)sender
{
    [gst_backend pause];
}

- (void)viewDidLayoutSubviews
{
    CGFloat view_width = video_container_view.bounds.size.width;
    CGFloat view_height = video_container_view.bounds.size.height;

    CGFloat correct_height = view_width * media_height / media_width;
    CGFloat correct_width = view_height * media_width / media_height;

    if (correct_height < view_height) {
        video_height_constraint.constant = correct_height;
        video_width_constraint.constant = view_width;
    } else {
        video_width_constraint.constant = correct_width;
        video_height_constraint.constant = view_height;
    }
}

/*
 * Methods from GstreamerBackendDelegate
 */

-(void) gstreamerInitialized
{
    dispatch_async(dispatch_get_main_queue(), ^{
        play_button.enabled = TRUE;
        pause_button.enabled = TRUE;
        message_label.text = @"Ready";
        //[gst_backend setUri:uri];
        //[gst_backend setUri:@"132"];
    });
}

-(void) gstreamerSetUIMessage:(NSString *)message
{
    dispatch_async(dispatch_get_main_queue(), ^{
        message_label.text = message;
    });
}

@end
