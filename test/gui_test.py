import time
import unittest
from unittest.mock import patch

import ttkbootstrap as ttk
from tkinter import messagebox, filedialog

from controller import Controller
from login_page import LoginPage


# from typing import Callable, Optional


class TestMainAppLogin(unittest.TestCase):
    def setUp(self):
        self.master = ttk.Window()
        # 控制器
        self.controller = Controller(self.master)

    def tearDown(self):
        # 延时销毁以避免 TclError
        self.master.after(100, self.master.destroy)
        # 确保足够的时间完成操作
        time.sleep(0.1)

    def test_login_page_elements(self):
        """Test if login page elements are present."""
        title = self.master.title()
        self.assertEquals("Order Management System", title)

        username_label = self.controller.login_page.nametowidget(self.controller.login_page.username_label)
        password_label = self.controller.login_page.nametowidget(self.controller.login_page.password_label)

        self.assertIsInstance(username_label, ttk.Label)
        self.assertIsInstance(password_label, ttk.Label)

        username_entry = self.controller.login_page.nametowidget(self.controller.login_page.username_entry)
        password_entry = self.controller.login_page.nametowidget(self.controller.login_page.password_entry)
        login_button = self.controller.login_page.nametowidget(self.controller.login_page.login_button)

        self.assertIsInstance(username_entry, ttk.Entry)
        self.assertIsInstance(password_entry, ttk.Entry)
        self.assertIsInstance(login_button, ttk.Button)

    def test_login_to_main(self):
        """Test if login transitions to the main page with correct username."""
        # Simulate entering username and password
        self.controller.login_page.username_entry.insert(0, "admin")
        self.controller.login_page.password_entry.insert(0, "1234")

        with patch("tkinter.messagebox.showinfo") as mock_showinfo:
            # Simulate button click with empty credentials
            self.controller.login_page.login_button.invoke()
            # Assert messagebox was called with correct arguments
            mock_showinfo.assert_called_once_with("Info", "Login successful")

        # 断言login_page有destroy
        login_page_winfo_exists = self.controller.login_page.winfo_exists()
        self.assertEquals(login_page_winfo_exists, False)

        # 判断main_application_page是否存在
        main_application_page_winfo_exists = self.controller.main_application_page.winfo_exists()
        self.assertEquals(main_application_page_winfo_exists, True)

        # 断言是否跳转到main_application_page
        # 断言main_application_page的title是否为Main Application
        main_application_page_title = self.master.title()
        self.assertEquals(main_application_page_title, "Main Application")

    def test_login_failed(self):
        """Test if login fails with incorrect credentials."""
        # Simulate entering incorrect username and password
        self.controller.login_page.username_entry.insert(0, "user")
        self.controller.login_page.password_entry.insert(0, "wrong_password")

        with patch("tkinter.messagebox.showerror") as mock_showerror:
            # Simulate button click with incorrect credentials
            self.controller.login_page.login_button.invoke()
            # Assert messagebox was called with correct arguments
            mock_showerror.assert_called_once_with("Error", "Login failed")

        # 断言login_page没有destroy
        login_page_winfo_exists = self.controller.login_page.winfo_exists()
        self.assertEquals(login_page_winfo_exists, True)

        # 断言main_application_page不存在
        main_application_page = self.controller.main_application_page
        self.assertEquals(main_application_page, None)

        # 断言没有跳转到main_application_page
        # 断言main_application_page的title 不是 Main Application
        main_application_page_title = self.master.title()
        self.assertEquals(main_application_page_title, "Order Management System")


if __name__ == "__main__":
    unittest.main()


#
# class TestPoisonDartCase(unittest.TestCase):
#
#     def setUp(self) -> None:
#         self.poison_dart = PoisonDart()
#
#     def test_get_name(self):
#         self.assertEquals(self.poison_dart.get_name(), 'PoisonDart')
#
#     def test_get_symbol(self):
#         self.assertEquals(self.poison_dart.get_symbol(), 'D')
#
#     def test_get_effect(self):
#         self.assertEquals(self.poison_dart.get_effect(), {'poison': 2})
#
#     def test_get_targets(self):
#         position = (1, 1)
#         self.assertEquals(self.poison_dart.get_targets(position),
#                           [(1, 2), (1, 0), (2, 1), (0, 1), (1, 3), (1, -1),
#                            (3, 1), (-1, 1)])
#         position = (8, 8)
#         self.assertEquals(self.poison_dart.get_targets(position),
#                           [(8, 9), (8, 7), (9, 8), (7, 8), (8, 10), (8, 6),
#                            (10, 8), (6, 8)])
#
#     def test_str(self):
#         self.assertEquals(str(self.poison_dart), 'PoisonDart')
#
#     def test_repr(self):
#         self.assertEquals(repr(self.poison_dart), 'PoisonDart()')
#
#
# class TestPoisonSwordCase(unittest.TestCase):
#
#     def setUp(self) -> None:
#         self.poison_sword = PoisonSword()
#
#     def test_get_name(self):
#         self.assertEquals(self.poison_sword.get_name(), 'PoisonSword')
#
#     def test_get_symbol(self):
#         self.assertEquals(self.poison_sword.get_symbol(), 'S')
#
#     def test_get_effect(self):
#         self.assertEquals(self.poison_sword.get_effect(),
#                           {'damage': 2, 'poison': 1})
#
#     def test_get_targets(self):
#         position = (1, 1)
#         self.assertEquals(self.poison_sword.get_targets(position),
#                           [(1, 2), (1, 0), (2, 1), (0, 1)])
#         position = (0, 0)
#         self.assertEquals(self.poison_sword.get_targets(position),
#                           [(0, 1), (0, -1), (1, 0), (-1, 0)])
#
#     def test_str(self):
#         self.assertEquals(str(self.poison_sword), 'PoisonSword')
#
#     def test_repr(self):
#         self.assertEquals(repr(self.poison_sword), 'PoisonSword()')
#
#
# class TestHealingRockCase(unittest.TestCase):
#
#     def setUp(self) -> None:
#         self.healing_rock = HealingRock()
#
#     def test_get_name(self):
#         self.assertEquals(self.healing_rock.get_name(), 'HealingRock')
#
#     def test_get_symbol(self):
#         self.assertEquals(self.healing_rock.get_symbol(), 'H')
#
#     def test_get_effect(self):
#         self.assertEquals(self.healing_rock.get_effect(), {'healing': 2})
#
#     def test_get_targets(self):
#         position = (1, 1)
#         self.assertEquals(self.healing_rock.get_targets(position),
#                           [(1, 2), (1, 0), (2, 1), (0, 1), (1, 3), (1, -1),
#                            (3, 1), (-1, 1)])
#
#     def test_str(self):
#         self.assertEquals(str(self.healing_rock), 'HealingRock')
#
#     def test_repr(self):
#         self.assertEquals(repr(self.healing_rock), 'HealingRock()')
#
#
# class TestTileCase(unittest.TestCase):
#
#     def setUp(self) -> None:
#         self.tile = Tile("#", True)
#
#     def test_is_blocking(self):
#         self.assertEquals(self.tile.is_blocking(), True)
#
#     def test_get_weapon(self):
#         self.assertEquals(self.tile.get_weapon(), None)
#
#     def test_get_weapon2(self):
#         healing_rock = HealingRock()
#         self.tile.set_weapon(healing_rock)
#         self.assertEquals(self.tile.get_weapon(), healing_rock)
#         self.assertEquals(self.tile.get_weapon().get_effect(), {'healing': 2})
#
#     def test_remove_weapon(self):
#         healing_rock = HealingRock()
#         self.tile.set_weapon(healing_rock)
#         self.assertEquals(self.tile.get_weapon(), healing_rock)
#         self.assertEquals(self.tile.get_weapon().get_effect(), {'healing': 2})
#         #
#         self.tile.remove_weapon()
#         self.assertEquals(self.tile.get_weapon(), None)
#
#     def test_str(self):
#         self.assertEquals(str(self.tile), '#')
#
#     def test_repr(self):
#         self.assertEquals(repr(self.tile), "Tile('#', True)")
#
#     def test_custom_repr(self):
#         tile = Tile("hello", False)
#         self.assertEquals(repr(tile), "Tile('hello', False)")
#         self.assertEquals(tile.is_blocking(), False)
#
#
# class TestCreateTileCase(unittest.TestCase):
#
#     def test_create_tile(self):
#         wall = create_tile('#')
#         self.assertEquals(repr(wall), "Tile('#', True)")
#         self.assertEquals(wall.is_blocking(), True)
#         self.assertEquals(wall.get_weapon(), None)
#         #
#         floor = create_tile(' ')
#         self.assertEquals(repr(floor), "Tile(' ', False)")
#         #
#         weapon_tile = create_tile('D')
#         self.assertEquals(repr(weapon_tile), "Tile(' ', False)")
#         self.assertEquals(repr(weapon_tile.get_weapon()), "PoisonDart()")
#
#
# class TestEntityCase(unittest.TestCase):
#
#     def setUp(self):
#         self.entity = Entity(10)
#
#     def test_get_symbol(self):
#         self.assertEquals(self.entity.get_symbol(), 'E')
#
#     def test_get_name(self):
#         self.assertEquals(self.entity.get_name(), 'Entity')
#
#     def test_get_poison(self):
#         self.assertEquals(self.entity.get_poison(), 0)
#
#     def test_get_weapon(self):
#         self.assertEquals(self.entity.get_weapon(), None)
#
#     def test_get_weapon_targets(self):
#         self.assertEquals(self.entity.get_weapon_targets((1, 1)), [])
#
#     def test_get_weapon_effect(self):
#         self.assertEquals(self.entity.get_weapon_effect(), {})
#
#     def test_equip(self):
#         poison_sword = PoisonSword()
#         self.entity.equip(poison_sword)
#         self.assertEquals(self.entity.get_weapon(), poison_sword)
#         self.assertEquals(self.entity.get_weapon_targets((0, 0)),
#                           [(0, 1), (0, -1), (1, 0), (-1, 0)])
#         self.assertEquals(self.entity.get_weapon_effect(),
#                           {'damage': 2, 'poison': 1})
#
#     def test_apply_effects_and_apply_poison(self):
#         self.entity.apply_effects({'poison': 4, 'damage': 3})
#         self.assertEquals(self.entity.get_health(), 7)
#         self.assertEquals(self.entity.get_poison(), 4)
#         #
#         self.entity.apply_poison()
#         self.assertEquals(self.entity.get_health(), 3)
#         self.assertEquals(self.entity.get_poison(), 3)
#         #
#         self.entity.apply_effects({'healing': 20})
#         self.assertEquals(self.entity.get_health(), 10)
#
#     def test_str(self):
#         self.assertEquals(str(self.entity), 'Entity')
#
#     def test_repr(self):
#         self.assertEquals(repr(self.entity), 'Entity(10)')
#
#
# class TestPlayerCase(unittest.TestCase):
#
#     def setUp(self):
#         self.player = Player(20)
#
#     def test_str(self):
#         self.assertEquals(str(self.player), 'Player')
#
#     def test_repr(self):
#         self.assertEquals(repr(self.player), 'Player(20)')
#
#     def test_equip_and_apply_effects(self):
#         poison_dart = PoisonDart()
#         self.player.equip(poison_dart)
#         self.assertEquals(self.player.get_weapon_effect(), {'poison': 2})
#         self.player.apply_effects({'damage': 25})
#         self.assertEquals(self.player.get_health(), 0)
#
#
# class TestSlugCase(unittest.TestCase):
#
#     def setUp(self):
#         self.slug = Slug(5)
#
#     def test_case(self):
#         healing_rock = HealingRock()
#         self.slug.equip(healing_rock)
#         self.assertEquals(self.slug.get_weapon_effect(), {'healing': 2})
#         #
#         self.assertEquals(self.slug.can_move(), True)
#         #
#         self.slug.end_turn()
#         self.assertEquals(self.slug.can_move(), False)
#         self.assertEquals(self.slug.can_move(), False)
#         self.slug.end_turn()
#         self.assertEquals(self.slug.can_move(), True)
#         #
#         try:
#             self.slug.choose_move([(0, 0), (1, 1)], (1, 0), (2, 4))
#         except NotImplementedError:
#             pass
#
#     def test_str(self):
#         self.assertEquals(str(self.slug), 'Slug')
#
#     def test_repr(self):
#         self.assertEquals(repr(self.slug), 'Slug(5)')
#
#
# class TestNiceSlugCase(unittest.TestCase):
#
#     def setUp(self):
#         self.nice_slug = NiceSlug()
#
#     def test_case(self):
#         self.assertEquals(repr(self.nice_slug), 'NiceSlug()')
#         #
#         self.assertEquals(str(self.nice_slug), 'NiceSlug')
#         #
#         self.assertEquals(self.nice_slug.get_health(), 10)
#         #
#         self.assertEquals(repr(self.nice_slug.get_weapon()), "HealingRock()")
#         #
#         self.assertEquals(self.nice_slug.get_weapon_effect(), {'healing': 2})
#         #
#         self.assertEquals(
#             self.nice_slug.choose_move([(0, 1), (1, 0), (1, 2), (2, 1)], (1, 1),
#                                        (2, 4)), (1, 1))
#
#
# class TestAngrySlugCase(unittest.TestCase):
#
#     def setUp(self):
#         self.angry_slug = AngrySlug()
#
#     def test_case(self):
#         self.assertEquals(repr(self.angry_slug), 'AngrySlug()')
#         #
#         self.assertEquals(str(self.angry_slug), 'AngrySlug')
#         #
#         self.assertEquals(self.angry_slug.get_health(), 5)
#         #
#         self.assertEquals(repr(self.angry_slug.get_weapon()), "PoisonSword()")
#         #
#         self.assertEquals(self.angry_slug.get_weapon_effect(),
#                           {'damage': 2, 'poison': 1})
#         #
#         self.assertEquals(
#             self.angry_slug.choose_move([(0, 1), (1, 0), (1, 2), (2, 1)],
#                                         (1, 1), (2, 4)), (1, 2))
#
#
# class TestScaredSlugCase(unittest.TestCase):
#
#     def setUp(self):
#         self.scared_slug = ScaredSlug()
#
#     def test_case(self):
#         self.assertEquals(repr(self.scared_slug), 'ScaredSlug()')
#         #
#         self.assertEquals(str(self.scared_slug), 'ScaredSlug')
#         #
#         self.assertEquals(self.scared_slug.get_health(), 3)
#         #
#         self.assertEquals(repr(self.scared_slug.get_weapon()), "PoisonDart()")
#         #
#         self.assertEquals(self.scared_slug.get_weapon_effect(), {'poison': 2})
#         #
#         self.assertEquals(
#             self.scared_slug.choose_move([(0, 1), (1, 0), (1, 2), (2, 1)],
#                                          (1, 1), (2, 4)), (1, 0))
#
#
# class TestSlugDungeonModelCase(unittest.TestCase):
#
#     def setUp(self):
#         self.tiles = [
#             [create_tile("#"), create_tile("#"), create_tile("#"),
#              create_tile("#")],
#             [create_tile("#"), create_tile(" "), create_tile(" "),
#              create_tile("#")],
#             [create_tile("#"), create_tile(" "), create_tile(" "),
#              create_tile("#")],
#             [create_tile("#"), create_tile("S"), create_tile("G"),
#              create_tile("#")],
#             [create_tile("#"), create_tile("#"), create_tile("#"),
#              create_tile("#")]
#         ]
#         self.slugs = {(1, 1): AngrySlug()}
#         self.player = Player(20)
#         self.model = SlugDungeonModel(self.tiles, self.slugs, self.player,
#                                       (2, 1))
#
#     def test_case(self):
#         self.assertEquals(self.model.get_tiles(), self.tiles)
#         #
#         self.assertEquals(self.model.get_slugs(), self.slugs)
#         #
#         self.assertEquals(repr(self.model.get_player()), "Player(20)")
#         #
#         self.assertEquals(self.model.get_player_position(), (2, 1))
#         #
#         self.assertEquals(repr(self.model.get_tile((0, 0))),
#                           repr(Tile('#', True)))
#         self.assertEquals(repr(self.model.get_tile((2, 1))),
#                           repr(Tile(' ', False)))
#         self.assertEquals(self.model.get_dimensions(), (5, 4)),
#         #
#         angry_slug = self.model.get_slugs().get((1, 1))
#         self.assertEquals(angry_slug.get_health(), 5)
#         self.assertEquals(angry_slug.get_weapon_effect(),
#                           {'damage': 2, 'poison': 1})
#         self.assertEquals(angry_slug.get_poison(), 0)
#         #
#         self.assertEquals(self.model.get_player().get_health(), 20)
#         self.assertEquals(self.model.get_player().get_poison(), 0)
#         self.assertEquals(self.model.get_player().get_weapon_effect(), {})
#         # TODO
#         # self.assertEquals(self.model.get_valid_slug_positions(angry_slug), [(1, 1), (1, 2)])
#         #
#         self.model.perform_attack(angry_slug, (1, 1))
#         self.assertEquals(self.model.get_player().get_health(), 18)
#         self.assertEquals(self.model.get_player().get_poison(), 1)
#         #
#         self.model.perform_attack(self.player, self.model.get_player_position())
#         self.assertEquals(angry_slug.get_health(), 5)
#         self.assertEquals(angry_slug.get_poison(), 0)
#         #
#         self.model.handle_player_move((1, 0))
#         self.assertEquals(self.model.get_player().get_health(), 15)
#         self.assertEquals(self.model.get_player().get_poison(), 1)
#         #
#         self.assertEquals(repr(self.player.get_weapon()),
#                           "PoisonSword()")  # Player picked up a weapon when it moved
#         self.assertEquals(self.model.get_player().get_weapon_effect(),
#                           {'damage': 2, 'poison': 1})
#         self.assertEquals(
#             self.player.get_weapon_targets(self.model.get_player_position()),
#             [(3, 2), (3, 0), (4, 1), (2, 1)])
#         #
#         self.assertEquals(angry_slug.get_health(), 5)
#         self.assertEquals(angry_slug.get_poison(), 0)
#         #
#         self.assertEquals(self.model.get_slugs(),
#                           self.slugs)  # {(2, 1): AngrySlug()}
#         self.assertEquals(self.model.get_player_position(), (3, 1))
#         #
#         self.assertEquals(self.model.has_won(), False)
#         self.assertEquals(self.model.has_lost(), False)
#
#     def test_end_turn(self):
#         model = load_level('levels/test_player_move')
#         slugs = {
#             (1, 3): ScaredSlug(),
#             (2, 1): NiceSlug(),
#             (2, 2): AngrySlug(),
#             (2, 4): ScaredSlug(),
#             (4, 2): AngrySlug(),
#         }
#         player = Player(25)
#
#         model2 = SlugDungeonModel(
#             model.get_tiles(), slugs, player, (1, 1)
#         )
#
#         # Preparing some poison for bottom angry slug
#         angry_slug_position = (4, 2)
#         angry_slug = model2.get_slugs().get(angry_slug_position)
#         angry_slug.apply_effects({"poison": 1000})
#
#         # Test bottom slug dies and drops weapon
#         model2.end_turn()
#         self.assertEquals(len(model2.get_slugs()), 4)
#         self.assertEquals(model2.get_tile((4, 2)).get_weapon().get_symbol(), "S")
#
#         # Test poison, healing and damage was applied to player
#         self.assertEquals(player.get_health(), 23)
#         self.assertEquals(player.get_poison(), 3)
#
#         # Test slug movement
#         self.assertEqual(
#             set(model2.get_slugs().keys()),
#             set([(2, 1), (1, 3), (1, 2), (2, 4)])
#         )
#
#         for slug in model2.get_slugs().values():
#             self.assertEquals(slug.can_move(), False)
#
#     def test_player_move(self):
#         model = load_level('levels/test_player_move')
#
#         slugs = {
#             (1, 3): ScaredSlug(),
#             (2, 1): NiceSlug(),
#             (2, 2): AngrySlug(),
#             (2, 4): ScaredSlug(),
#             (4, 2): AngrySlug(),
#         }
#         player = Player(25)
#
#         model2 = SlugDungeonModel(
#             model.get_tiles(), slugs, player, (1, 1)
#         )
#
#         # Setup sword to player right
#         sword = PoisonSword()
#         tile_to_right = model2.get_tile((1, 2))
#         tile_to_right.set_weapon(sword)
#
#         # Player moves right
#         player.apply_effects({"poison": 1, "damage": 5})
#         model2.handle_player_move((0, 1))
#         self.assertNotEqual(model2.get_slugs(), slugs)
#         self.assertEquals(player.get_health(), 25 - 5 - 2 - 1)
#
#         # Assert that player damaged the enemies
#         self.assertEquals(len(model2.get_slugs()), 4)
#         angry_slug_position = (2, 2)
#         angry_slug = model2.get_slugs().get(angry_slug_position)
#         self.assertEquals(angry_slug.get_health(), 2)