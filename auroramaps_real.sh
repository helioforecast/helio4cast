cd /nas/helio/real_time_test/
source bin/activate
echo
echo 'using the real_time_test virtual environment'
which python
echo '--------------------------------------------'
echo

cd /nas/helio/real_time_test/auroramaps
/nas/helio/real_time_test/bin/python /nas/helio/real_time_test/auroramaps/aurora.py  --server --real
