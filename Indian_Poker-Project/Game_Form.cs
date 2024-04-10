using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Indian_Poker
{
    public partial class Game_Form : Form
    {
        Indian_PokerG indian;
        public Game_Form()
        {
            InitializeComponent();
            indian = new Indian_PokerG();
        }
        public void setControlText()
        {
            label3.Text = indian.bat_chip.ToString(); // 배팅칩
            label5.Text = indian.user_chip.ToString(); // 사용자 칩
            label7.Text = indian.com_chip.ToString(); // 상대방 칩
            label8.Text = indian.com_card.ToString(); // 상대방 숫자카드
        }
        public void setA_com()
        {
            label9.Text = "선공 : 상대방";
            indian.bating(0, 5);
            numericUpDown1.Value = 5;
            button1.Enabled = false;
        }
        public void setA_user()
        {
            label9.Text = "선공 : 사용자";
            button1.Enabled = true;
        }
        private void button1_Click(object sender, EventArgs e)
        {
            // 배팅 버튼
            bool co; 
            co = indian.bating(1, numericUpDown1.Value);
            if (!co)
                MessageBox.Show("상대방보다 혹은 사용자가 보유한 칩보다 더 많이 배팅할 수 없습니다!", "Bating Error");
            else
            {
                indian.bating(0, numericUpDown1.Value);
                setControlText();
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            // 콜 버튼
            indian.bating(1, numericUpDown1.Value);
            button1.Enabled = true;
            setControlText();
        }

        private void button3_Click(object sender, EventArgs e)
        {
            // 다이 버튼
            if (indian.bat_chip == 2)
            {
                // 게임 시작 후 초기에 상대방의 카드를 보고 죽기를 확정했다면
                // 바로 5개의 칩을 상대방에서 줘야 한다.
                indian.bating(1, 5);
                indian.game_Win(0);
                setControlText();
            }
            else if (indian.bat_chip == 7)
            {
                // 맨 처음 게임이 시작되고 상대방이 선공일 때 반드시 5개를 베팅하게 되는 상황이다.
                // 이럴 때 콜을 누르지 않고 다이를 누른다면 마찬가지로 5개의 칩을 넘겨줘야 한다.
                indian.bating(1, 5);
                indian.game_Win(0);
                setControlText();
            }
            else
            {
                // 2보다 크다는 의미는 이미 콜을 여러번 해서 배팅 칩이 어느정도 쌓인 상태인데
                // 이럴 때 죽으면 그냥 배팅 된 칩을 상대방에서 모두 준다.
                indian.game_Win(0);
                setControlText();
            }
            textBox1.Text = $"사용자가 die 했습니다. 카드를 오픈합니다.\r\n" + indian.result();
            label8.Text = "패배";
            indian.num = 0;
            button1.Enabled = false; // 배팅 버튼 비활성화
            button2.Enabled = false; // 콜 버튼 비활성화
            button3.Enabled = false; // 다이 버튼 비활성화
            button4.Enabled = true; // Next 버튼 활성화
            button5.Enabled = false; // Open 버튼 비활성화
        }
        private void button4_Click(object sender, EventArgs e)
        {
            // Next Button
            indian.settingCard();
            if (indian.num == 0)
                setA_com();
            else
                setA_user();
            setControlText();
            textBox1.Clear();
            button4.Enabled = false; // Next버튼 비활성화
            button2.Enabled = true; // Call버튼 비활성화
            button3.Enabled = true; // Die버튼 비활성화
            button5.Enabled = true; // Open버튼 비활성화
        }

        private void button5_Click(object sender, EventArgs e)
        {
            // Open Button
            string msg = $"카드를 오픈합니다.\r\n" + indian.result();
            textBox1.Text = msg;
            if (indian.com_card > indian.user_card)
            {
                indian.game_Win(0);
                indian.num = 0;
                textBox1.Text = msg + "상대방의 승리입니다!";
                setControlText();
                label8.Text = "패배...";
            }
            else if (indian.user_card > indian.com_card)
            {
                indian.game_Win(1);
                indian.num = 1;
                textBox1.Text = msg + "사용자의 승리입니다!";
                setControlText();
                label8.Text = "승리!";
            }
            else
            {
                indian.game_Draw();
                textBox1.Text = msg + "무승부입니다!";
                setControlText();
                label8.Text = "무승부!";
            }
            button1.Enabled = false; // 배팅 버튼 비활성화
            button2.Enabled = false; // 콜 버튼 비활성화
            button3.Enabled = false; // 다이 버튼 비활성화
            button4.Enabled = true; // Next 버튼 활성화
            button5.Enabled = false; // Open 버튼 비활성화
        }
        private void Game_Form_Load(object sender, EventArgs e)
        {
            indian.settingCard();
            indian.setAttack();
            if (indian.num == 0)
                setA_com();
            else
                setA_user();
            button4.Enabled = false; // Next키를 잠금
            setControlText();
        }

        private void button6_Click(object sender, EventArgs e) => Dispose();
    }
}
