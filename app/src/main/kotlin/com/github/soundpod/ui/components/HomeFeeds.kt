package com.github.musick.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil3.compose.AsyncImage

data class FeedItemMock(val id: String, val title: String, val subtitle: String, val thumbnailUrl: String)

@Composable
fun SpeedDialGrid(items: List<FeedItemMock>, onItemClick: (String) -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 16.dp)
    ) {
        Text(
            text = "Speed Dial",
            style = MaterialTheme.typography.titleLarge.copy(
                fontWeight = FontWeight.ExtraBold, 
                fontSize = 24.sp,
                letterSpacing = (-0.5).sp
            ),
            color = MaterialTheme.colorScheme.onBackground,
            modifier = Modifier.padding(horizontal = 16.dp)
        )
        Spacer(modifier = Modifier.height(14.dp))
        
        // اسکرول افقی بی‌نهایت با تقسيم‌بندی ۲تایی
        LazyRow(
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            // لیست رو به گروه‌های ۲ تایی می‌شکنیم تا دقیقاً ۲ سطر بشه
            items(items.chunked(2)) { columnItems ->
                Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    for (item in columnItems) {
                        SpeedDialCard(
                            item = item, 
                            onClick = { onItemClick(item.id) }, 
                            // عرض ثابت ۱۳۰dp تا اسکرول نرم و یکدست باشه
                            modifier = Modifier.width(130.dp)
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun SpeedDialCard(item: FeedItemMock, onClick: () -> Unit, modifier: Modifier = Modifier) {
    Box(
        modifier = modifier
            .aspectRatio(1f) // فرم مستطیلی کاورها
            .clip(RoundedCornerShape(14.dp))
            .clickable { onClick() }
    ) {
        // ۱. لایه زیرین: عکس کاور
        AsyncImage(
            model = item.thumbnailUrl,
            contentDescription = item.title,
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )
        
        // ۲. لایه میانی: گرادیانت تاریک برای خوانایی متن (از بی‌رنگ به مشکی)
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(
                    Brush.verticalGradient(
                        colors = listOf(Color.Black.copy(alpha = 0.1f), Color.Black.copy(alpha = 0.85f)),
                        startY = 0f
                    )
                )
        )
        
        // ۳. لایه رویی: متن‌ها در مرکز کاور
        Column(
            modifier = Modifier
                .align(Alignment.Center)
                .padding(8.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Text(
                text = item.title, 
                fontSize = 14.sp, 
                fontWeight = FontWeight.ExtraBold, 
                maxLines = 2, 
                overflow = TextOverflow.Ellipsis, 
                color = Color.White, // همیشه سفید تا روی کاور دیده بشه
                textAlign = TextAlign.Center
            )
            
            Text(
                text = item.subtitle, 
                fontSize = 10.sp, 
                fontWeight = FontWeight.Medium,
                maxLines = 1, 
                overflow = TextOverflow.Ellipsis, 
                color = Color.White.copy(alpha = 0.75f),
                textAlign = TextAlign.Center
            )
        }
    }
}
