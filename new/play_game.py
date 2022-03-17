import connect_four as cf
import connect_four_Algorithm as CFA

cf_object = cf.Connect_Four(log = True)
cf_Algorithm = CFA.Connect_four_algorithm()

cf_object.play_game(cf_object.real_player_opencv, cf_Algorithm.min_max_alpha_beta_player, log = True)