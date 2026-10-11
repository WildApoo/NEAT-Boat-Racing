# code entièrement généré par ia
import pygame
from bateau import Bateau
from UserInterface.arbreGenealogique import createArbreGenealogique

# Initialisation globale pour les polices
pygame.init()
FONT_UI = pygame.font.SysFont("Consolas", 20, bold=True)
# Police pour les numéros (ajustée à la taille des carrés)
FONT_BATEAU = pygame.font.SysFont("Arial", 18, bold=True)

# Variables pour mémoriser le cadrage une seule fois (Statique)
_STATED_SCALE = None
_STATED_MIN_MAX = None

def dessiner_pygame(bateaux, checkpoints, epoch, temps_actuel, temps_total, width=1000, height=800):
    global _STATED_SCALE, _STATED_MIN_MAX
    
    screen = pygame.display.get_surface()
    if screen is None:
        screen = pygame.display.set_mode((width, height))
    
    # --- CALCUL DU CADRAGE FIXE ---
    if _STATED_SCALE is None:
        cp_x = [cp.x for cp in checkpoints]
        cp_y = [cp.y for cp in checkpoints]
        min_x, max_x = min(cp_x), max(cp_x)
        min_y, max_y = min(cp_y), max(cp_y)
        
        padding = 80
        range_x = max(1, max_x - min_x)
        range_y = max(1, max_y - min_y)
        
        scale_x = (width - 2 * padding) / range_x
        scale_y = (height - 2 * padding) / range_y
        _STATED_SCALE = min(scale_x, scale_y)
        _STATED_MIN_MAX = (min_x, min_y)

    def to_px(x, y):
        assert _STATED_MIN_MAX is not None and _STATED_SCALE is not None
        m_x, m_y = _STATED_MIN_MAX
        px = int(80 + (x - m_x) * _STATED_SCALE)
        py = int(height - (80 + (y - m_y) * _STATED_SCALE))
        return px, py

    # --- RENDU ---
    screen.fill((30, 30, 30)) 

    # 1. Dessiner les Checkpoints
    for cp in checkpoints:
        px, py = to_px(cp.x, cp.y)
        pygame.draw.circle(screen, (231, 76, 60), (px, py), 12)
        pygame.draw.circle(screen, (255, 255, 255), (px, py), 12, 2)
        label = FONT_UI.render(str(cp.name), True, (200, 200, 200))
        screen.blit(label, (px + 15, py - 15))

    # --- CALCULS POUR L'OPACITÉ ---
    scores = [b.score for b in bateaux]
    max_s = max(scores) if scores else 1
    min_s = min(scores) if scores else 0
    range_s = max_s - min_s

    # 2. Dessiner les Bateaux
    for i, b in enumerate(bateaux):
        bx, by = to_px(b.x, b.y)
        
        if 0 <= bx <= width and 0 <= by <= height:
            taille = 30
            # Création de la surface pour la transparence (SRCALPHA)
            surf = pygame.Surface((taille, taille), pygame.SRCALPHA)
            
            # Calcul de l'alpha (255 = 100%, 25 = 10%)
            if range_s > 0:
                # Normalisation entre 25 (min) et 255 (max)
                alpha = 25 + ((b.score - min_s) / range_s) * (255 - 25)
            else:
                alpha = 255
            alpha = int(alpha)

            # Détermination de la couleur selon tes paliers
            if i < len(bateaux) / 10:
                color = (46, 204, 113, alpha)  # Vert
                thick = 2
            elif (i > len(bateaux) / 2) and (i < (len(bateaux) / 2 + len(bateaux) / 10)):
                color = (255, 44, 44, alpha)   # Rouge
                thick = 2
            else:
                color = (52, 152, 219, alpha)  # Bleu
                thick = 1
            
            # Dessin du carré sur la surface temporaire
            rect_temp = pygame.Rect(0, 0, taille, taille)
            pygame.draw.rect(surf, color, rect_temp)
            pygame.draw.rect(surf, (255, 255, 255, alpha), rect_temp, thick)

            # Ajout du texte sur la surface temporaire
            # On change la couleur du texte pour le contraste (Noir sur Vert, Blanc ailleurs)
            text_color = (0, 0, 0, alpha) if i < len(bateaux)/10 else (255, 255, 255, alpha)
            txt_num = FONT_BATEAU.render(str(i), True, text_color[:3])
            txt_num.set_alpha(alpha) # Applique la transparence au texte
            
            txt_rect = txt_num.get_rect(center=(taille // 2, taille // 2))
            surf.blit(txt_num, txt_rect)

            # Blit de la surface finale sur l'écran
            screen.blit(surf, (bx - taille // 2, by - taille // 2))

    # 3. Interface
    header_rect = pygame.Rect(0, 0, width, 40)
    pygame.draw.rect(screen, (50, 50, 50), header_rect)
    
    info_str = f" EPOQUE: {epoch:03} | TEMPS: {temps_actuel}/{temps_total} | POP: {len(bateaux)}"
    text_surface = FONT_UI.render(info_str, True, (46, 204, 113))
    screen.blit(text_surface, (10, 8))

    pygame.display.flip()
    
    # 4. Timing (Remis à 15 FPS comme demandé précédemment)
    pygame.time.Clock().tick(5) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


def show_heredity(bateaux: list[Bateau], width=1200, height=800, fullscreen=False):
    """
    Affiche l'arbre généalogique avec une racine visible, une hiérarchie plus lisible
    et des séparations d'époque en arrière-plan.
    """
    screen = pygame.display.get_surface()
    import colorsys
    if fullscreen:
        display_info = pygame.display.Info()
        width = display_info.current_w
        height = display_info.current_h - 60
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    elif screen is None:
        screen = pygame.display.set_mode((width, height))

    FONT_NODE = pygame.font.SysFont("Arial", 14, bold=True)
    FONT_UI = pygame.font.SysFont("Consolas", 16)

    if not bateaux:
        return

    max_epoch = max(len(b.cerveau.heredity) for b in bateaux)
    arbre_racine = createArbreGenealogique(bateaux)

    node_start_epochs = {arbre_racine: -1}
    parent_map = {}
    all_nodes = [arbre_racine]

    def traverse(noeud, start_ep):
        for ep in sorted(noeud.enfants.keys()):
            for enfant in noeud.enfants[ep]:
                node_start_epochs[enfant] = ep
                parent_map[enfant] = noeud
                all_nodes.append(enfant)
                traverse(enfant, ep)

    traverse(arbre_racine, -1)

    descendant_counts = {}

    def count_descendants(node):
        if node in descendant_counts:
            return descendant_counts[node]
        count = 0
        for enfants_list in node.enfants.values():
            for enfant in enfants_list:
                count += 1 + count_descendants(enfant)
        descendant_counts[node] = count
        return count

    for node in all_nodes:
        count_descendants(node)

    max_descendants = max(descendant_counts.values()) if descendant_counts else 1

    top_level_children = []
    for ep in sorted(arbre_racine.enfants.keys()):
        for enfant in arbre_racine.enfants[ep]:
            top_level_children.append(enfant)
            
    family_colors = {}
    node_to_family = {}
    family_max_epochs = {}
    node_max_reach = {arbre_racine: max_epoch - 1}
    
    hue_step = 1.0 / max(1, len(top_level_children))
    for i, tlc in enumerate(top_level_children):
        r, g, b = colorsys.hsv_to_rgb(i * hue_step, 0.8, 0.9)
        family_colors[tlc] = (int(r*255), int(g*255), int(b*255))
        
    def populate_family(node, tlc):
        node_to_family[node] = tlc
        max_ep = node_start_epochs.get(node, 0)
        for ep in sorted(node.enfants.keys()):
            for enfant in node.enfants[ep]:
                child_max = populate_family(enfant, tlc)
                max_ep = max(max_ep, child_max)
        node_max_reach[node] = max_ep
        return max_ep
        
    for tlc in top_level_children:
        family_max_epochs[tlc] = populate_family(tlc, tlc)
        if family_max_epochs[tlc] < max_epoch - 1:
            orig = family_colors[tlc]
            h, s, v = colorsys.rgb_to_hsv(orig[0]/255.0, orig[1]/255.0, orig[2]/255.0)
            r, g, b = colorsys.hsv_to_rgb(h, 0.2, 0.5)
            family_colors[tlc] = (int(r*255), int(g*255), int(b*255))

    search_matches = []
    search_index = 0

    class GroupedNode:
        def __init__(self, parent, count, epoch):
            self.num = f"+{count}"
            self.is_grouped = True
            self.text = f"{count} enfants" if count > 1 else f"{count} enfant"
            self.enfants = {}
            self.parent = parent
            self.epoch = epoch
            
    grouped_nodes_cache = {}

    root_y = 72
    epoch_origin_y = 180
    epoch_gap = 125
    node_width = 46
    sibling_gap = 12

    def get_children(node, visible_nodes_set):
        enfants = []
        effective_max_epoch = max_epoch - 1 if show_true_last_gen else max_epoch - 2
        for ep in sorted(node.enfants.keys()):
            if not detail_last_gen and ep == effective_max_epoch:
                visibles = [enfant for enfant in node.enfants[ep] if getattr(enfant, 'is_grouped', False) or enfant in visible_nodes_set]
                if visibles:
                    if (node, ep) not in grouped_nodes_cache:
                        gnode = GroupedNode(node, len(visibles), ep)
                        grouped_nodes_cache[(node, ep)] = gnode
                        node_start_epochs[gnode] = ep
                        descendant_counts[gnode] = 0
                        
                        fam_node = None
                        for v in visibles:
                            if v in node_to_family:
                                fam_node = node_to_family[v]
                                break
                        if fam_node is not None:
                            node_to_family[gnode] = fam_node
                    else:
                        gnode = grouped_nodes_cache[(node, ep)]
                        gnode.num = f"+{len(visibles)}"
                        gnode.text = f"{len(visibles)} enfants" if len(visibles) > 1 else f"{len(visibles)} enfant"
                        descendant_counts[gnode] = 0
                    
                    enfants.append((ep, gnode))
            else:
                for enfant in node.enfants[ep]:
                    if enfant in visible_nodes_set:
                        enfants.append((ep, enfant))
        enfants.sort(key=lambda item: (-descendant_counts.get(item[1], 0), getattr(item[1], 'num', ''), item[0]))
        return enfants

    def recalculate_layout(visible_nodes_set):
        positions = {}
        width_cache = {}

        def subtree_width(node):
            if not getattr(node, 'is_grouped', False) and node not in visible_nodes_set:
                return 0
            if node in width_cache:
                return width_cache[node]

            children = get_children(node, visible_nodes_set)
            if not children:
                width_cache[node] = node_width
                return node_width

            total = 0
            for index, (_, child) in enumerate(children):
                total += subtree_width(child)
                if index < len(children) - 1:
                    total += sibling_gap

            width_cache[node] = max(node_width, total)
            return width_cache[node]

        def assign_positions(node, left_x, right_x):
            if not getattr(node, 'is_grouped', False) and node not in visible_nodes_set:
                return

            x = (left_x + right_x) / 2
            epoch = node_start_epochs.get(node, -1)
            y = root_y if epoch < 0 else epoch_origin_y + (epoch * epoch_gap)
            positions[node] = (x, y)

            children = get_children(node, visible_nodes_set)
            if not children:
                return

            total_children_width = 0
            for index, (_, child) in enumerate(children):
                total_children_width += subtree_width(child)
                if index < len(children) - 1:
                    total_children_width += sibling_gap

            cursor_x = x - (total_children_width / 2)
            for index, (_, child) in enumerate(children):
                child_width = subtree_width(child)
                assign_positions(child, cursor_x, cursor_x + child_width)
                cursor_x += child_width
                if index < len(children) - 1:
                    cursor_x += sibling_gap

        assign_positions(arbre_racine, 0, max(node_width, subtree_width(arbre_racine)))
        return positions

    def get_screen_pos(world_x, world_y, camera_x, camera_y, zoom):
        return (
            int(TREE_DRAW_X + ((world_x - camera_x) * zoom)),
            int(TREE_DRAW_Y + ((world_y - camera_y) * zoom)),
        )

    def get_world_pos(screen_x, screen_y, camera_x, camera_y, zoom):
        return (
            (screen_x - TREE_DRAW_X) / zoom + camera_x,
            (screen_y - TREE_DRAW_Y) / zoom + camera_y,
        )

    running = True
    clock = pygame.time.Clock()
    camera_x, camera_y = 0, 0
    zoom = 1.0
    is_dragging = False
    last_mouse_pos = (0, 0)

    selected_lineage = set()
    search_epoch = ""
    search_id = ""
    active_input = None

    rect_search_epoch = pygame.Rect(width - 250, 10, 100, 30)
    rect_search_id = pygame.Rect(width - 120, 10, 100, 30)
    rect_zoom_in = pygame.Rect(10, 60, 40, 40)
    rect_zoom_out = pygame.Rect(60, 60, 40, 40)

    PANEL_W = 310
    HEADER_H = 50
    VIEW_PAD = 14
    TREE_VIEW_X = PANEL_W
    TREE_VIEW_Y = HEADER_H
    TREE_VIEW_W = max(1, width - TREE_VIEW_X)
    TREE_VIEW_H = max(1, height - TREE_VIEW_Y)
    TREE_DRAW_X = TREE_VIEW_X + VIEW_PAD
    TREE_DRAW_Y = TREE_VIEW_Y + VIEW_PAD
    TREE_DRAW_W = max(1, TREE_VIEW_W - (VIEW_PAD * 2) - 12)
    TREE_DRAW_H = max(1, TREE_VIEW_H - (VIEW_PAD * 2) - 12)

    rect_filter_epoch = pygame.Rect(18, HEADER_H + 68, PANEL_W - 36, 34)
    rect_filter_id = pygame.Rect(18, HEADER_H + 132, PANEL_W - 36, 34)
    rect_apply_filters = pygame.Rect(18, HEADER_H + 190, PANEL_W - 36, 38)
    rect_prev_btn = pygame.Rect(18, HEADER_H + 240, (PANEL_W - 46) // 2, 34)
    rect_next_btn = pygame.Rect(18 + (PANEL_W - 46) // 2 + 10, HEADER_H + 240, (PANEL_W - 46) // 2, 34)

    show_living_families = True
    show_extinct_families = True
    show_dead_ends = False
    detail_last_gen = True
    show_true_last_gen = False
    
    rect_cb_living = pygame.Rect(18, HEADER_H + 340, 20, 20)
    rect_cb_extinct = pygame.Rect(18, HEADER_H + 370, 20, 20)
    rect_cb_deadends = pygame.Rect(18, HEADER_H + 400, 20, 20)
    rect_cb_detail_last_gen = pygame.Rect(18, HEADER_H + 430, 20, 20)
    rect_cb_show_true_last_gen = pygame.Rect(18, HEADER_H + 460, 20, 20)

    filter_epoch_input = ""
    filter_id_input = ""
    applied_filter_epoch = ""
    applied_filter_id = ""
    filter_feedback = "Aucun filtre appliqué"

    base_visible_nodes = set(all_nodes)
    current_visible_nodes = set(all_nodes)
    layout_bounds = (0, 1, 0, 1)

    def select_branch(start_node):
        lineage = {start_node, arbre_racine}

        a_visiter = [start_node]
        while a_visiter:
            courant = a_visiter.pop(0)
            for enfants_list in courant.enfants.values():
                for enfant in enfants_list:
                    if enfant not in lineage:
                        lineage.add(enfant)
                        a_visiter.append(enfant)

        a_visiter = [start_node]
        while a_visiter:
            courant = a_visiter.pop(0)
            if courant in parent_map:
                parent = parent_map[courant]
                if parent not in lineage:
                    lineage.add(parent)
                    a_visiter.append(parent)

        return lineage

    def get_layout_bounds(positions):
        if not positions:
            return (0, 1, 0, 1)

        xs = [pos[0] for pos in positions.values()]
        ys = [pos[1] for pos in positions.values()]
        padding = 70
        return (min(xs) - padding, max(xs) + padding, min(ys) - padding, max(ys) + padding)

    def parse_epoch_value(text):
        text = text.strip()
        if not text:
            return None
        try:
            return int(text)
        except ValueError:
            return None

    def build_visible_nodes(epoch_text, id_text):
        epoch_value = parse_epoch_value(epoch_text)
        node_id_value = id_text.strip()

        if epoch_value is None and not node_id_value:
            return set(all_nodes)

        matches = []
        for node in all_nodes:
            if node is arbre_racine:
                continue

            node_epoch = node_start_epochs.get(node)
            if epoch_value is not None and node_epoch != epoch_value:
                continue
            if node_id_value and str(node.num) != node_id_value:
                continue

            matches.append(node)

        visible = set()
        for node in matches:
            visible |= select_branch(node)

        return visible

    def clamp_camera_to_bounds():
        nonlocal camera_x, camera_y

        min_x, max_x, min_y, max_y = layout_bounds
        view_w = TREE_DRAW_W / zoom
        view_h = TREE_DRAW_H / zoom
        content_w = max_x - min_x
        content_h = max_y - min_y

        if content_w <= view_w:
            camera_x = min_x + (content_w - view_w) / 2
        else:
            camera_x = min(max(camera_x, min_x), max_x - view_w)

        if content_h <= view_h:
            camera_y = min_y + (content_h - view_h) / 2
        else:
            camera_y = min(max(camera_y, min_y), max_y - view_h)

    def get_active_visible_nodes():
        if selected_lineage:
            return base_visible_nodes & selected_lineage
        return set(base_visible_nodes)

    def refresh_visible_layout():
        nonlocal current_visible_nodes, current_positions, layout_bounds
        current_visible_nodes = get_active_visible_nodes()
        current_positions = recalculate_layout(current_visible_nodes)
        layout_bounds = get_layout_bounds(current_positions)
        clamp_camera_to_bounds()

    def update_base_visible_nodes():
        nonlocal base_visible_nodes
        base_visible_nodes = set()
        for node in all_nodes:
            if not show_true_last_gen and node_start_epochs.get(node) == max_epoch - 1:
                continue

            if node is arbre_racine:
                base_visible_nodes.add(node)
                continue
            
            tlc = node_to_family.get(node)
            is_extinct = family_max_epochs.get(tlc, 0) < max_epoch - 1 if tlc else False
            
            if is_extinct and not show_extinct_families:
                continue
            
            if not is_extinct and not show_living_families:
                continue
                
            if not show_dead_ends:
                target_reach = family_max_epochs.get(tlc, max_epoch - 1) if tlc else max_epoch - 1
                if node_max_reach.get(node, 0) < target_reach:
                    continue
                    
            base_visible_nodes.add(node)
            
        refresh_visible_layout()

    def go_to_search_result():
        nonlocal camera_x, camera_y
        if not search_matches:
            return
        node = search_matches[search_index]
        if node in current_positions:
            wx, wy = current_positions[node]
            view_w = TREE_DRAW_W / zoom
            view_h = TREE_DRAW_H / zoom
            camera_x = wx - view_w / 2
            camera_y = wy - view_h / 2
            clamp_camera_to_bounds()

    def apply_filters():
        nonlocal applied_filter_epoch, applied_filter_id, base_visible_nodes, filter_feedback, search_matches, search_index

        applied_filter_epoch = filter_epoch_input.strip()
        applied_filter_id = filter_id_input.strip()
        search_matches.clear()
        search_index = 0

        # Search inside visible nodes to avoid jumping to hidden sections
        epoch_value = parse_epoch_value(applied_filter_epoch)
        if epoch_value is not None or applied_filter_id:
            for node in base_visible_nodes:
                if node is arbre_racine: continue
                node_ep = node_start_epochs.get(node)
                if epoch_value is not None and node_ep != epoch_value: continue
                if applied_filter_id and str(node.num) != applied_filter_id: continue
                search_matches.append(node)

        if applied_filter_epoch or applied_filter_id:
            if search_matches:
                filter_feedback = f"Trouvé: {len(search_matches)} noeud(s)"
                go_to_search_result()
            else:
                filter_feedback = "Aucun résultat"
        else:
            filter_feedback = "Aucun filtre appliqué"

        selected_lineage.clear()
        refresh_visible_layout()

    def compute_scrollbars():
        min_x, max_x, min_y, max_y = layout_bounds
        view_w = TREE_DRAW_W / zoom
        view_h = TREE_DRAW_H / zoom
        content_w = max_x - min_x
        content_h = max_y - min_y

        track_right = pygame.Rect(TREE_VIEW_X + TREE_VIEW_W - 12, TREE_VIEW_Y + 10, 8, TREE_VIEW_H - 20)
        track_bottom = pygame.Rect(TREE_VIEW_X + 10, TREE_VIEW_Y + TREE_VIEW_H - 12, TREE_VIEW_W - 20, 8)

        if content_w <= view_w:
            thumb_w = track_bottom.width
            thumb_x = track_bottom.x
        else:
            thumb_w = max(40, int(track_bottom.width * (view_w / content_w)))
            thumb_range = max(1, track_bottom.width - thumb_w)
            ratio_x = (camera_x - min_x) / max(1, content_w - view_w)
            ratio_x = max(0.0, min(1.0, ratio_x))
            thumb_x = track_bottom.x + int(thumb_range * ratio_x)

        if content_h <= view_h:
            thumb_h = track_right.height
            thumb_y = track_right.y
        else:
            thumb_h = max(40, int(track_right.height * (view_h / content_h)))
            thumb_range = max(1, track_right.height - thumb_h)
            ratio_y = (camera_y - min_y) / max(1, content_h - view_h)
            ratio_y = max(0.0, min(1.0, ratio_y))
            thumb_y = track_right.y + int(thumb_range * ratio_y)

        return {
            "track_right": track_right,
            "track_bottom": track_bottom,
            "thumb_right": pygame.Rect(track_right.x, thumb_y, track_right.width, thumb_h),
            "thumb_bottom": pygame.Rect(thumb_x, track_bottom.y, thumb_w, track_bottom.height),
            "content_w": content_w,
            "content_h": content_h,
            "view_w": view_w,
            "view_h": view_h,
            "min_x": min_x,
            "min_y": min_y,
        }

    def set_camera_from_scrollbar_x(mouse_x, scrollbar_state, drag_offset_x):
        nonlocal camera_x

        if scrollbar_state["content_w"] <= scrollbar_state["view_w"]:
            return

        track = scrollbar_state["track_bottom"]
        thumb = scrollbar_state["thumb_bottom"]
        thumb_range = max(1, track.width - thumb.width)
        ratio = (mouse_x - track.x - drag_offset_x) / thumb_range
        ratio = max(0.0, min(1.0, ratio))
        camera_x = scrollbar_state["min_x"] + ratio * max(1, scrollbar_state["content_w"] - scrollbar_state["view_w"])
        clamp_camera_to_bounds()

    def set_camera_from_scrollbar_y(mouse_y, scrollbar_state, drag_offset_y):
        nonlocal camera_y

        if scrollbar_state["content_h"] <= scrollbar_state["view_h"]:
            return

        track = scrollbar_state["track_right"]
        thumb = scrollbar_state["thumb_right"]
        thumb_range = max(1, track.height - thumb.height)
        ratio = (mouse_y - track.y - drag_offset_y) / thumb_range
        ratio = max(0.0, min(1.0, ratio))
        camera_y = scrollbar_state["min_y"] + ratio * max(1, scrollbar_state["content_h"] - scrollbar_state["view_h"])
        clamp_camera_to_bounds()

    def draw_epoch_background():
        for ep in range(max_epoch):
            center_y = epoch_origin_y + (ep * epoch_gap)
            top_y = int(center_y - (epoch_gap / 2))
            top_screen_y = int(TREE_DRAW_Y + ((top_y - camera_y) * zoom))
            band_height = max(1, int(epoch_gap * zoom))
            band_color = (32, 34, 40) if ep % 2 == 0 else (27, 29, 34)
            pygame.draw.rect(screen, band_color, pygame.Rect(TREE_DRAW_X, top_screen_y, TREE_DRAW_W, band_height))
            pygame.draw.line(screen, (76, 80, 90), (TREE_DRAW_X, top_screen_y), (TREE_DRAW_X + TREE_DRAW_W, top_screen_y), 1)
            pygame.draw.line(screen, (40, 43, 49), (TREE_DRAW_X, top_screen_y + band_height), (TREE_DRAW_X + TREE_DRAW_W, top_screen_y + band_height), 1)
            label = FONT_UI.render(f"époque {ep}", True, (155, 162, 176))
            screen.blit(label, (TREE_DRAW_X + 12, top_screen_y + 8))

        root_line_y = int(TREE_DRAW_Y + ((root_y + 30 - camera_y) * zoom))
        pygame.draw.line(screen, (90, 95, 105), (TREE_DRAW_X, root_line_y), (TREE_DRAW_X + TREE_DRAW_W, root_line_y), 1)

    def draw_edge(parent, child, index_epoch):
        if parent not in current_positions or child not in current_positions:
            return

        px, py = get_screen_pos(current_positions[parent][0], current_positions[parent][1], camera_x, camera_y, zoom)
        cx, cy = get_screen_pos(current_positions[child][0], current_positions[child][1], camera_x, camera_y, zoom)

        if selected_lineage:
            color = (52, 152, 219) if (parent in selected_lineage and child in selected_lineage) else (45, 47, 54)
        else:
            if child in node_to_family and node_to_family[child] in family_colors:
                color = family_colors[node_to_family[child]]
            else:
                color = (100, 110, 125)

        width_line_base = max(1, int(1.5 * zoom + (descendant_counts.get(child, 0) / max_descendants) * 8 * zoom))
        width_line = max(1, int(4 * zoom)) if selected_lineage else width_line_base
        direction = 1 if cy >= py else -1
        max_offset = max(22, abs(cy - py) // 2 - 12)
        lane_offset = min(max_offset, 18 + (index_epoch * 10))
        mid_y = py + (direction * lane_offset)

        pygame.draw.line(screen, color, (px, py), (px, mid_y), width_line)
        pygame.draw.line(screen, color, (px, mid_y), (cx, mid_y), width_line)
        pygame.draw.line(screen, color, (cx, mid_y), (cx, cy), width_line)

    update_base_visible_nodes()
    current_positions = recalculate_layout(current_visible_nodes)
    layout_bounds = get_layout_bounds(current_positions)
    clamp_camera_to_bounds()

    scrollbar_state = compute_scrollbars()
    scroll_drag_axis = None
    scroll_drag_offset_x = 0
    scroll_drag_offset_y = 0

    while running:
        screen.fill((26, 27, 31))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        scrollbar_state = compute_scrollbars()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEWHEEL:
                old_world_x, old_world_y = get_world_pos(mouse_x, mouse_y, camera_x, camera_y, zoom)
                if event.y > 0:
                    zoom = min(zoom * 1.1, 3.0)
                else:
                    zoom = max(zoom * 0.9, 0.2)
                new_world_x, new_world_y = get_world_pos(mouse_x, mouse_y, camera_x, camera_y, zoom)
                camera_x -= (new_world_x - old_world_x)
                camera_y -= (new_world_y - old_world_y)
                clamp_camera_to_bounds()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if scrollbar_state["thumb_bottom"].collidepoint(event.pos):
                        scroll_drag_axis = "x"
                        scroll_drag_offset_x = event.pos[0] - scrollbar_state["thumb_bottom"].x
                        continue
                    if scrollbar_state["thumb_right"].collidepoint(event.pos):
                        scroll_drag_axis = "y"
                        scroll_drag_offset_y = event.pos[1] - scrollbar_state["thumb_right"].y
                        continue

                    if scrollbar_state["track_bottom"].collidepoint(event.pos):
                        scroll_drag_axis = "x"
                        scroll_drag_offset_x = scrollbar_state["thumb_bottom"].width // 2
                        set_camera_from_scrollbar_x(event.pos[0], scrollbar_state, scroll_drag_offset_x)
                        continue
                    if scrollbar_state["track_right"].collidepoint(event.pos):
                        scroll_drag_axis = "y"
                        scroll_drag_offset_y = scrollbar_state["thumb_right"].height // 2
                        set_camera_from_scrollbar_y(event.pos[1], scrollbar_state, scroll_drag_offset_y)
                        continue

                    if rect_apply_filters.collidepoint(event.pos):
                        apply_filters()
                        continue

                    if search_matches and rect_prev_btn.collidepoint(event.pos):
                        search_index = (search_index - 1) % len(search_matches)
                        filter_feedback = f"Résultat {search_index + 1}/{len(search_matches)}"
                        go_to_search_result()
                        continue
                    if search_matches and rect_next_btn.collidepoint(event.pos):
                        search_index = (search_index + 1) % len(search_matches)
                        filter_feedback = f"Résultat {search_index + 1}/{len(search_matches)}"
                        go_to_search_result()
                        continue

                    if getattr(event, 'button', 0) == 1:
                        if rect_cb_living.collidepoint(event.pos):
                            show_living_families = not show_living_families
                            update_base_visible_nodes()
                            continue
                        if rect_cb_extinct.collidepoint(event.pos):
                            show_extinct_families = not show_extinct_families
                            update_base_visible_nodes()
                            continue
                        if rect_cb_deadends.collidepoint(event.pos):
                            show_dead_ends = not show_dead_ends
                            update_base_visible_nodes()
                            continue
                        if rect_cb_detail_last_gen.collidepoint(event.pos):
                            detail_last_gen = not detail_last_gen
                            current_positions = recalculate_layout(current_visible_nodes)
                            layout_bounds = get_layout_bounds(current_positions)
                            clamp_camera_to_bounds()
                            continue
                        if rect_cb_show_true_last_gen.collidepoint(event.pos):
                            show_true_last_gen = not show_true_last_gen
                            update_base_visible_nodes()
                            continue

                    if rect_zoom_in.collidepoint(event.pos):
                        zoom = min(zoom * 1.2, 3.0)
                        clamp_camera_to_bounds()
                        continue
                    if rect_zoom_out.collidepoint(event.pos):
                        zoom = max(zoom * 0.8, 0.2)
                        clamp_camera_to_bounds()
                        continue
                    if rect_filter_epoch.collidepoint(event.pos):
                        active_input = "epoch"
                        continue
                    if rect_filter_id.collidepoint(event.pos):
                        active_input = "id"
                        continue

                    active_input = None

                    if event.pos[0] < TREE_VIEW_X:
                        continue

                    node_clicked = False
                    rayon = 16 * zoom
                    for node, (wx, wy) in current_positions.items():
                        sx, sy = get_screen_pos(wx, wy, camera_x, camera_y, zoom)
                        if (mouse_x - sx) ** 2 + (mouse_y - sy) ** 2 <= rayon ** 2:
                            node_clicked = True
                            if selected_lineage and node in selected_lineage:
                                selected_lineage.clear()
                            else:
                                selected_lineage = select_branch(node)
                            refresh_visible_layout()
                            break

                    if not node_clicked:
                        is_dragging = True
                        last_mouse_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_dragging = False
                    scroll_drag_axis = None

            elif event.type == pygame.MOUSEMOTION:
                if scroll_drag_axis == "x":
                    set_camera_from_scrollbar_x(mouse_x, scrollbar_state, scroll_drag_offset_x)
                elif scroll_drag_axis == "y":
                    set_camera_from_scrollbar_y(mouse_y, scrollbar_state, scroll_drag_offset_y)
                elif is_dragging:
                    dx = mouse_x - last_mouse_pos[0]
                    dy = mouse_y - last_mouse_pos[1]
                    camera_x -= dx / zoom
                    camera_y -= dy / zoom
                    last_mouse_pos = (mouse_x, mouse_y)
                    clamp_camera_to_bounds()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    selected_lineage.clear()
                    refresh_visible_layout()
                    continue

                if event.key == pygame.K_RETURN:
                    if active_input in {"epoch", "id"}:
                        apply_filters()
                        continue

                if active_input == "epoch":
                    if event.key == pygame.K_BACKSPACE:
                        filter_epoch_input = filter_epoch_input[:-1]
                    elif event.unicode.isnumeric():
                        filter_epoch_input += event.unicode
                elif active_input == "id":
                    if event.key == pygame.K_BACKSPACE:
                        filter_id_input = filter_id_input[:-1]
                    elif event.unicode.isalnum():
                        filter_id_input += event.unicode

        current_visible_nodes = get_active_visible_nodes()
        current_positions = recalculate_layout(current_visible_nodes)
        layout_bounds = get_layout_bounds(current_positions)
        clamp_camera_to_bounds()
        scrollbar_state = compute_scrollbars()

        tree_clip = pygame.Rect(TREE_VIEW_X, TREE_VIEW_Y, TREE_VIEW_W, TREE_VIEW_H)
        screen.set_clip(tree_clip)
        pygame.draw.rect(screen, (24, 26, 31), tree_clip)
        draw_epoch_background()

        for parent in all_nodes:
            if not getattr(parent, 'is_grouped', False) and parent not in current_visible_nodes:
                continue

            children_edges = get_children(parent, current_visible_nodes)
            for index_edge, (_, enfant) in enumerate(children_edges):
                if enfant in current_positions:
                    draw_edge(parent, enfant, index_edge)

        rayon_base = 15
        for node, (wx, wy) in current_positions.items():
            epoque = node_start_epochs[node]
            node_id = str(node.num)
            sx, sy = get_screen_pos(wx, wy, camera_x, camera_y, zoom)

            if sx < TREE_VIEW_X - 50 or sx > width + 50 or sy < TREE_VIEW_Y - 50 or sy > height + 50:
                continue

            ratio_succes = descendant_counts.get(node, 0) / max_descendants if max_descendants > 0 else 0

            if node is arbre_racine:
                couleur_cercle = (230, 196, 78)
                couleur_bordure = (255, 235, 160)
                couleur_texte = (28, 24, 8)
                rayon = max(int(rayon_base * zoom) + 5, 22)
            elif search_matches and node == search_matches[search_index]:
                # POINT RECHERCHÉ SELECTIONNÉ
                couleur_cercle = (255, 0, 0)
                couleur_bordure = (255, 255, 255)
                couleur_texte = (255, 255, 255)
                rayon = int(rayon_base * zoom) + 8
            elif node in search_matches:
                # AUTRES POINTS DE LA RECHERCHE
                couleur_cercle = (255, 165, 0)
                couleur_bordure = (255, 255, 255)
                couleur_texte = (0, 0, 0)
                rayon = int(rayon_base * zoom) + 4
            else:
                if node in node_to_family and node_to_family[node] in family_colors:
                    couleur_cercle = family_colors[node_to_family[node]]
                    couleur_bordure = (200, 205, 210) if ratio_succes > 0 else (80, 85, 95)
                    # Text luminosity logic
                    lum = 0.299 * couleur_cercle[0] + 0.587 * couleur_cercle[1] + 0.114 * couleur_cercle[2]
                    couleur_texte = (0, 0, 0) if lum > 128 else (255, 255, 255)
                else:
                    r = int(40 + ratio_succes * (46 - 40))
                    g = int(50 + ratio_succes * (204 - 50))
                    b = int(70 + ratio_succes * (113 - 70))
                    couleur_cercle = (r, g, b)
                    couleur_texte = (255, 255, 255) if ratio_succes < 0.6 else (0, 0, 0)
                    couleur_bordure = (200, 205, 210) if ratio_succes > 0 else (80, 85, 95)
                rayon = int(rayon_base * zoom)

            pygame.draw.circle(screen, couleur_cercle, (sx, sy), rayon)
            pygame.draw.circle(screen, couleur_bordure, (sx, sy), rayon, max(1, int(2 * zoom)))

            if zoom > 0.35:
                label = "racine" if node is arbre_racine else node_id
                txt = FONT_NODE.render(label, True, couleur_texte)
                txt_rect = txt.get_rect(center=(sx, sy))
                screen.blit(txt, txt_rect)

        screen.set_clip(None)

        panel_rect = pygame.Rect(0, HEADER_H, PANEL_W, height - HEADER_H)
        pygame.draw.rect(screen, (18, 19, 22), panel_rect)
        pygame.draw.line(screen, (56, 59, 66), (PANEL_W, HEADER_H), (PANEL_W, height), 1)

        header_rect = pygame.Rect(0, 0, width, HEADER_H)
        pygame.draw.rect(screen, (18, 19, 22), header_rect)
        pygame.draw.line(screen, (80, 80, 80), (0, HEADER_H), (width, HEADER_H))

        info_txt = FONT_UI.render(
            f"ARBRE GENEALOGIQUE (CONDENSÉ) | Epoques Max: {max_epoch} | Focus: {'ACTIF' if selected_lineage else 'GLOBAL'}",
            True, (220, 220, 220))
        screen.blit(info_txt, (PANEL_W + 10, 15))

        pygame.draw.rect(screen, (70, 70, 70), rect_zoom_in, border_radius=5)
        screen.blit(FONT_UI.render("+", True, (255, 255, 255)), (rect_zoom_in.x + 15, rect_zoom_in.y + 10))
        pygame.draw.rect(screen, (70, 70, 70), rect_zoom_out, border_radius=5)
        screen.blit(FONT_UI.render("-", True, (255, 255, 255)), (rect_zoom_out.x + 15, rect_zoom_out.y + 10))

        panel_title = FONT_UI.render("Filtres", True, (240, 240, 240))
        screen.blit(panel_title, (18, HEADER_H + 18))

        label_epoch = FONT_UI.render("Epoque", True, (190, 196, 205))
        screen.blit(label_epoch, (18, HEADER_H + 48))
        pygame.draw.rect(screen, (42, 44, 50) if active_input == "epoch" else (30, 32, 37), rect_filter_epoch, border_radius=6)
        pygame.draw.rect(screen, (110, 116, 128), rect_filter_epoch, 1, border_radius=6)
        screen.blit(FONT_UI.render(filter_epoch_input or "ex: 3", True, (255, 255, 255) if filter_epoch_input else (130, 136, 145)), (rect_filter_epoch.x + 8, rect_filter_epoch.y + 7))

        label_id = FONT_UI.render("Noeud", True, (190, 196, 205))
        screen.blit(label_id, (18, HEADER_H + 112))
        pygame.draw.rect(screen, (42, 44, 50) if active_input == "id" else (30, 32, 37), rect_filter_id, border_radius=6)
        pygame.draw.rect(screen, (110, 116, 128), rect_filter_id, 1, border_radius=6)
        screen.blit(FONT_UI.render(filter_id_input or "ex: 61", True, (255, 255, 255) if filter_id_input else (130, 136, 145)), (rect_filter_id.x + 8, rect_filter_id.y + 7))

        pygame.draw.rect(screen, (68, 111, 173), rect_apply_filters, border_radius=8)
        pygame.draw.rect(screen, (136, 170, 230), rect_apply_filters, 1, border_radius=8)
        apply_label = FONT_UI.render("Rechercher", True, (255, 255, 255))
        apply_rect = apply_label.get_rect(center=rect_apply_filters.center)
        screen.blit(apply_label, apply_rect)
        
        if search_matches:
            pygame.draw.rect(screen, (80, 85, 95), rect_prev_btn, border_radius=8)
            label_prev = FONT_UI.render("< Prec", True, (255, 255, 255))
            screen.blit(label_prev, label_prev.get_rect(center=rect_prev_btn.center))

            pygame.draw.rect(screen, (80, 85, 95), rect_next_btn, border_radius=8)
            label_next = FONT_UI.render("Suiv >", True, (255, 255, 255))
            screen.blit(label_next, label_next.get_rect(center=rect_next_btn.center))

        status_label = FONT_UI.render(filter_feedback, True, (160, 166, 176))
        screen.blit(status_label, (18, HEADER_H + 280))

        # --- DRAW CHECKBOXES ---
        opt_title = FONT_UI.render("Options d'Affichage", True, (240, 240, 240))
        screen.blit(opt_title, (18, HEADER_H + 310))

        def draw_cb(rect, is_checked, label_text):
            pygame.draw.rect(screen, (30, 32, 37), rect, border_radius=4)
            pygame.draw.rect(screen, (110, 116, 128), rect, 1, border_radius=4)
            if is_checked:
                pygame.draw.line(screen, (46, 204, 113), (rect.x + 4, rect.y + 10), (rect.x + 8, rect.y + 15), 2)
                pygame.draw.line(screen, (46, 204, 113), (rect.x + 8, rect.y + 15), (rect.x + 16, rect.y + 4), 2)
            lbl = FONT_UI.render(label_text, True, (190, 196, 205))
            screen.blit(lbl, (rect.right + 10, rect.top))

        draw_cb(rect_cb_living, show_living_families, "Familles en vie")
        draw_cb(rect_cb_extinct, show_extinct_families, "Familles éteintes")
        draw_cb(rect_cb_deadends, show_dead_ends, "Noeuds sans enfants")
        draw_cb(rect_cb_detail_last_gen, detail_last_gen, "Détail dernière génération")
        draw_cb(rect_cb_show_true_last_gen, show_true_last_gen, "Génération en cours vs simulée")

        hint_label = FONT_UI.render("Entrée valide = appliquer", True, (120, 125, 135))
        screen.blit(hint_label, (18, height - 30))

        v_track = scrollbar_state["track_right"]
        h_track = scrollbar_state["track_bottom"]
        v_thumb = scrollbar_state["thumb_right"]
        h_thumb = scrollbar_state["thumb_bottom"]

        pygame.draw.rect(screen, (40, 42, 47), h_track, border_radius=4)
        pygame.draw.rect(screen, (72, 78, 88), h_thumb, border_radius=4)
        pygame.draw.rect(screen, (40, 42, 47), v_track, border_radius=4)
        pygame.draw.rect(screen, (72, 78, 88), v_thumb, border_radius=4)

        pygame.display.flip()
        clock.tick(30)