import unittest
from unittest.mock import patch, Mock

from gitlord import phase4_done

class TestPhase4Done(unittest.TestCase):
    @patch('gitlord.run_git')
    @patch('gitlord.detect_default_branch')
    @patch('gitlord.get_current_branch')
    @patch('gitlord.print_phase_header')
    @patch('gitlord.print_info')
    @patch('gitlord.print_success')
    def test_phase4_done_existing_branch(self, mock_success, mock_info, mock_phase_header, mock_get_branch, mock_detect_branch, mock_run_git):
        # Setup mocks
        mock_detect_branch.return_value = "main"
        mock_get_branch.return_value = "main"
        mock_run_git.return_value = Mock(returncode=0)

        # Call function
        phase4_done()

        # Assertions
        mock_phase_header.assert_called_once_with(4, "Switch to master/main and pull latest")
        mock_info.assert_any_call("Detected default branch: main")
        mock_run_git.assert_any_call(["checkout", "main"], check=False)
        mock_run_git.assert_any_call(["pull", "origin", "main"])
        mock_success.assert_called_once_with("Now on branch 'main' with latest changes pulled.")

    @patch('gitlord.run_git')
    @patch('gitlord.detect_default_branch')
    @patch('gitlord.get_current_branch')
    def test_phase4_done_create_branch(self, mock_get_branch, mock_detect_branch, mock_run_git):
        # Simulate branch does not exist locally
        mock_detect_branch.return_value = "master"
        mock_get_branch.return_value = "master"
        mock_run_git.side_effect = [
            Mock(returncode=1),  # checkout returns error
            None,  # checkout -b runs
            None  # pull runs
        ]

        phase4_done()

        # Check if checkout -b called
        mock_run_git.assert_any_call(["checkout", "-b", "master", "origin/master"])

    @patch('gitlord.run_git')
    @patch('gitlord.detect_default_branch')
    @patch('gitlord.get_current_branch')
    def test_phase4_done_branch_switch_fail(self, mock_get_branch, mock_detect_branch, mock_run_git):
        mock_detect_branch.return_value = "main"
        mock_get_branch.return_value = "not-main"
        mock_run_git.return_value = Mock(returncode=0)

        with self.assertRaises(RuntimeError):
            phase4_done()

if __name__ == '__main__':
    unittest.main()
