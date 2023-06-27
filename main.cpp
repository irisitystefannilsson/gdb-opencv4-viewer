#include <opencv2/opencv.hpp>
#include <vector>
#include <string>

using namespace std;
using namespace cv;

int main(int argc, char *argv[])
{
  Mat img_color, img_gray, img_roi;
  img_color  = imread("../lena.png");
  cvtColor(img_color, img_gray, cv::COLOR_BGR2GRAY);
  
  int arr[] = {1,2,3,4,5,6};
  vector<int> vec(arr, arr+6);
  
  map<string, int> str_int_map;
  str_int_map[string("one")] = 1;
  str_int_map[string("two")] = 2;
  str_int_map[string("three")] = 3;
  
  vector<Mat> img_vec;
  img_vec.push_back(img_color);
  img_vec.push_back(img_gray);
  
  Rect rect(500, 600, 500, 500);
  img_roi = img_color(rect);
  
  return 0;
}
